# DK = Piyasa Değeri x R x K x H x G
def hesapla_deger_kaybi(
    piyasa_degeri,
    rayic_katsayisi,
    km_katsayisi,
    genel_katsayi,
    parca_kodu,
    islem_turu,
    hasar_seviyesi
):
    """Tüm parametrelerle değer kaybı hesapla."""
    parca_katsayi = get_parca_katsayi(parca_kodu, islem_turu, hasar_seviyesi)
    dk = piyasa_degeri * rayic_katsayisi * km_katsayisi * parca_katsayi * genel_katsayi
    return dk
def get_parca_katsayi(parca_kodu, islem_turu, hasar_seviyesi):
    """Parça kodu, işlem türü ve hasar seviyesine göre katsayıyı döndür."""
    # islem_turu: "degisim" veya "onarim"
    # hasar_seviyesi: "hafif", "orta", "yuksek"
    try:
        return PARCA_KATSAYI_TABLOSU[parca_kodu][islem_turu][hasar_seviyesi]
    except Exception:
        return 1.0  # Bulunamazsa nötr katsayı
# Parça/işlem/hasar katsayı tablosu (örnek, tamamı doldurulmalı)
# Format: {"PARCA_KODU": {"degisim": {"hafif": katsayi, "orta": katsayi, "yuksek": katsayi}, "onarim": {"hafif": katsayi, ...}}}
PARCA_KATSAYI_TABLOSU = {
    "A.1": {
        "degisim": {"hafif": 1.00, "orta": 1.00, "yuksek": 1.00},
        "onarim": {"hafif": 1.00, "orta": 1.00, "yuksek": 1.00},
    },
    "A.2": {
        "degisim": {"hafif": 2.00, "orta": 2.00, "yuksek": 2.00},
        "onarim": {"hafif": 2.00, "orta": 2.00, "yuksek": 2.00},
    },
    # ... (Tüm parçalar ve katsayılar tabloya göre doldurulmalı)
}
"""
KNN Model with Optuna Hyperparameter Optimization
-------------------------------------------------
Sadece KNN modeli için:
- Optuna ile hiperparametre optimizasyonu (k, metric, feature weights, distance weighting)
- Bin-filtered KNN (aynı bin içinde arama)
- Distance-weighted prediction
- K-Fold Cross-Validation
- Aynı veri hazırlama pipeline'ı (xgb_optuna_knn_v2.py ile uyumlu)
"""

import os
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import optuna
from optuna.samplers import TPESampler

# Veri seti yolu
EXCEL_PATH = "tamam_son_2.xlsx"
TARGET_COL = "deger_kaybi_miktari"
MISSING_CAT_TOKEN = "__MISSING__"

# Optuna optimizasyon ayarları
OPTUNA_N_TRIALS = 100  # KNN için deneme sayısı
OPTUNA_TIMEOUT = 3600  # 1 saat timeout (saniye)
CV_FOLDS = 5  # K-Fold CV için fold sayısı

# KNN ayarları (varsayılan)
KNN_DEFAULT_K = 5
KNN_METRICS = ['euclidean', 'manhattan', 'minkowski', 'chebyshev']

# Rayiç bin sınırları
RAYIC_BIN_BOUNDARIES = [
    (float('-inf'), 400000),      # bin1
    (400000, 580250),              # bin2
    (580250, 900000),              # bin3
    (900000, float('inf')),        # bin4
]

# KNN için kullanılacak özellikler (fallback ile)
KNN_FEATURES = [
    "rayic_bedel",
    "hasar_bedeli",
    "degisen_parca_sayisi",
    "onarilan_parca_sayisi",
    "arac_kilometresi",  # Öncelik: arac_kilometresi, fallback: km_k
]

# Numeric sütunlar
NUMERIC_CANDIDATES = [
    "rayic_bedel",
    "hasar_bedeli",
    "degisen_parca_sayisi",
    "onarilan_parca_sayisi",
    "dk_harici_parca_sayisi",
    "arac_kilometresi",
    "km_k",
    "parca_toplam",
    "degisen_oran",
    "islem_siddeti",
    "hasar_orani",
    "parca_basi_hasar",
    "arac_yasi",
    "hasar_skoru",
    "degisen_hafif_parca_sayisi",
    "degisen_hasar_skoru",
    "onarilan_hasar_skoru",
    "toplam_hasar_skoru",
]

# Boolean sütunlar
BOOLEAN_COLUMNS = [
    "gecmis_agir_hasar",
    "agir_dk_riski",
    "orta_dk_riski",
    "dusuk_dk_riski",
    "arac_tipi_motor",
    "arac_tipi_binek",
    "arac_tipi_otobus",
    "arac_tipi_luks",
    "arac_tipi_ticari",
    "tramer_kaydi",
]

# Eğitimde kullanılmayacak kolonlar
DROP_FEATURES = ["dosya_adi", "dosya adı", "dosyaAdi", "file_name", "filename", 
                 "bilirkisi_ad_soyad", "hakem_adi", "sigorta_sirketi", "sigorta_sirketi_norm",
                 "hasar_skor_detay", "hasar_skor_detayi"]


def to_numeric_tr(series: pd.Series) -> pd.Series:
    """Türkçe formatlı sayıları numeric'e çevir"""
    if series.dtype != "object":
        return pd.to_numeric(series, errors="coerce")
    s = series.astype(str).str.strip()
    s = s.replace({"": np.nan, "None": np.nan, "nan": np.nan})
    s = s.str.replace(".", "", regex=False)
    s = s.str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


def safe_div(a, b):
    """Güvenli bölme: a / (b + 1)"""
    return a / (b + 1)


def get_rayic_bin_idx(rayic_value):
    """Rayiç değerine göre bin numarasını döndür (1-4)"""
    if pd.isna(rayic_value):
        return 1
    for bin_idx, (min_val, max_val) in enumerate(RAYIC_BIN_BOUNDARIES, start=1):
        if min_val < rayic_value <= max_val:
            return bin_idx
    return 1


def get_rayic_bin_label(val):
    """Rayiç değerine göre bin label'ını döndür (string)"""
    if pd.isna(val):
        return "<=400k"
    val = float(val)
    if val <= 400000:
        return "<=400k"
    elif val <= 580250:
        return "400k-580.25k"
    elif val <= 900000:
        return "580.25k-900k"
    else:
        return ">900k"


def engineer_features(df):
    """
    Feature engineering: Domain-driven özellikler ekle
    """
    df = df.copy()
    
    # hasar_rayic_orani
    if "hasar_bedeli" in df.columns and "rayic_bedel" in df.columns:
        df["hasar_rayic_orani"] = safe_div(
            df["hasar_bedeli"].fillna(0),
            df["rayic_bedel"].fillna(1)
        )
    
    # islem_toplam
    if "degisen_parca_sayisi" in df.columns and "onarilan_parca_sayisi" in df.columns:
        df["islem_toplam"] = (
            df["degisen_parca_sayisi"].fillna(0) + 
            df["onarilan_parca_sayisi"].fillna(0)
        )
    
    # degisen_onarilan_oran
    if "degisen_parca_sayisi" in df.columns and "onarilan_parca_sayisi" in df.columns:
        df["degisen_onarilan_oran"] = safe_div(
            df["degisen_parca_sayisi"].fillna(0),
            df["onarilan_parca_sayisi"].fillna(0)
        )
    
    # parca_basi_hasar
    if "hasar_bedeli" in df.columns and "islem_toplam" in df.columns:
        df["parca_basi_hasar"] = safe_div(
            df["hasar_bedeli"].fillna(0),
            df["islem_toplam"]
        )
    elif "hasar_bedeli" in df.columns and "degisen_parca_sayisi" in df.columns and "onarilan_parca_sayisi" in df.columns:
        islem_toplam = df["degisen_parca_sayisi"].fillna(0) + df["onarilan_parca_sayisi"].fillna(0)
        df["parca_basi_hasar"] = safe_div(df["hasar_bedeli"].fillna(0), islem_toplam)
    
    # log_km
    km_col = None
    if "arac_kilometresi" in df.columns:
        km_col = "arac_kilometresi"
    elif "km_k" in df.columns:
        km_col = "km_k"
    
    if km_col:
        df["log_km"] = np.log1p(df[km_col].fillna(0))
    
    # parca_toplam
    if "parca_toplam" not in df.columns:
        if "degisen_parca_sayisi" in df.columns and "onarilan_parca_sayisi" in df.columns:
            df["parca_toplam"] = (
                df["degisen_parca_sayisi"].fillna(0) + 
                df["onarilan_parca_sayisi"].fillna(0)
            )
        elif "dk_harici_parca_sayisi" in df.columns:
            df["parca_toplam"] = df["dk_harici_parca_sayisi"].fillna(0)
        else:
            df["parca_toplam"] = 0
    
    # hasar_orani
    if "hasar_orani" not in df.columns:
        if "hasar_bedeli" in df.columns and "rayic_bedel" in df.columns:
            df["hasar_orani"] = safe_div(
                df["hasar_bedeli"].fillna(0),
                df["rayic_bedel"].fillna(1)
            )
        else:
            df["hasar_orani"] = 0
    
    # degisen_oran
    if "degisen_oran" not in df.columns:
        if "degisen_parca_sayisi" in df.columns and "parca_toplam" in df.columns:
            df["degisen_oran"] = safe_div(
                df["degisen_parca_sayisi"].fillna(0),
                df["parca_toplam"].fillna(1)
            )
        else:
            df["degisen_oran"] = 0
    
    # islem_siddeti
    if "islem_siddeti" not in df.columns:
        if "islem_toplam" in df.columns and "parca_toplam" in df.columns:
            df["islem_siddeti"] = safe_div(
                df["islem_toplam"].fillna(0),
                df["parca_toplam"].fillna(1)
            )
        elif "degisen_parca_sayisi" in df.columns and "onarilan_parca_sayisi" in df.columns:
            islem_toplam = df["degisen_parca_sayisi"].fillna(0) + df["onarilan_parca_sayisi"].fillna(0)
            if "parca_toplam" in df.columns:
                df["islem_siddeti"] = safe_div(islem_toplam, df["parca_toplam"].fillna(1))
            else:
                df["islem_siddeti"] = islem_toplam
        else:
            df["islem_siddeti"] = 0
    
    # tramer_x_hasar
    if "tramer_kaydi" in df.columns and "hasar_rayic_orani" in df.columns:
        tramer_val = df["tramer_kaydi"].copy()
        if tramer_val.dtype == 'object':
            tramer_val = tramer_val.astype(str).str.strip().str.lower()
            tramer_val = tramer_val.replace(['var', 'evet', 'yes', '1', 'true'], 1)
            tramer_val = tramer_val.replace(['yok', 'hayır', 'no', '0', 'false', ''], 0)
            tramer_val = pd.to_numeric(tramer_val, errors='coerce').fillna(0)
        df["tramer_x_hasar"] = (
            tramer_val.fillna(0).astype(int) * 
            df["hasar_rayic_orani"].fillna(0)
        )
    
    return df


def predict_knn(X_train, y_train, X_test, k, metric, feature_weights, 
                 use_distance_weighting=True, bin_idx=None):
    """
    KNN tahmin fonksiyonu
    
    Args:
        X_train: Eğitim özellikleri (DataFrame)
        y_train: Eğitim hedef değişkeni (Series)
        X_test: Test özellikleri (DataFrame, tek satır)
        k: Komşu sayısı
        metric: Mesafe metriği
        feature_weights: Özellik ağırlıkları (dict veya array)
        use_distance_weighting: Mesafe ağırlıklı tahmin kullanılsın mı?
        bin_idx: Bin numarası (filtreleme için)
    
    Returns:
        dict: Tahmin sonuçları ve istatistikler
    """
    if len(X_train) < k:
        k = len(X_train)
    
    if k == 0:
        return {'tahmin': 0, 'confidence': 0.0}
    
    # Özellik ağırlıklarını hazırla
    if isinstance(feature_weights, dict):
        feature_weights_array = np.array([feature_weights.get(f, 1.0) for f in X_train.columns])
    else:
        feature_weights_array = np.array(feature_weights)
    
    # Standardize et
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Ağırlıkları uygula
    X_train_weighted = X_train_scaled * feature_weights_array
    X_test_weighted = X_test_scaled * feature_weights_array
    
    # KNN modeli
    knn = NearestNeighbors(n_neighbors=k, metric=metric)
    knn.fit(X_train_weighted)
    
    # En yakın komşuları bul
    distances, indices = knn.kneighbors(X_test_weighted)
    
    # Distance-weighted prediction
    eps = 1e-10
    if use_distance_weighting:
        weights = 1.0 / (distances[0] + eps)
        weights = weights / weights.sum()  # Normalize
    else:
        weights = np.ones(len(distances[0])) / len(distances[0])  # Uniform
    
    # Target değerlerini al
    target_values = y_train.iloc[indices[0]].values
    
    # Weighted mean
    weighted_mean = np.sum(weights * target_values)
    
    # Confidence: mean similarity (inverse distance normalized)
    max_dist = distances[0].max() + eps
    similarities = 1.0 - (distances[0] / max_dist)
    confidence = similarities.mean()
    
    stats = {
        'tahmin': weighted_mean,
        'min': target_values.min(),
        'max': target_values.max(),
        'median': np.median(target_values),
        'std': target_values.std(),
        'sayi': len(target_values),
        'confidence': confidence,
        'distances': distances[0].tolist(),
        'weights': weights.tolist()
    }
    
    return stats


def objective_knn_cv(trial, df_train, target_col, bin_idx=None, cv_folds=CV_FOLDS):
    """
    KNN için Optuna objective function (K-Fold CV)
    
    Args:
        trial: Optuna trial
        df_train: Eğitim verisi DataFrame
        target_col: Hedef değişken adı
        bin_idx: Bin numarası (filtreleme için)
        cv_folds: CV fold sayısı
    
    Returns:
        float: CV MAE (ortalama)
    """
    # Bin filtreleme
    df_train_filtered = df_train.copy()
    if bin_idx is not None and "rayic_bedel" in df_train_filtered.columns:
        min_val, max_val = RAYIC_BIN_BOUNDARIES[bin_idx - 1]
        if min_val == float('-inf'):
            df_train_filtered = df_train_filtered[df_train_filtered["rayic_bedel"] <= max_val]
        elif max_val == float('inf'):
            df_train_filtered = df_train_filtered[df_train_filtered["rayic_bedel"] > min_val]
        else:
            df_train_filtered = df_train_filtered[
                (df_train_filtered["rayic_bedel"] > min_val) & 
                (df_train_filtered["rayic_bedel"] <= max_val)
            ]
    
    if len(df_train_filtered) < cv_folds:
        return float('inf')
    
    # KNN için kullanılacak özellikleri seç
    available_features = []
    for feat in KNN_FEATURES:
        if feat in df_train_filtered.columns:
            available_features.append(feat)
        elif feat == "arac_kilometresi" and "arac_kilometresi" not in df_train_filtered.columns:
            if "km_k" in df_train_filtered.columns:
                available_features.append("km_k")
    
    if len(available_features) == 0:
        return float('inf')
    
    # Hiperparametreler
    k = trial.suggest_int('k', 3, min(50, len(df_train_filtered) // 2))
    metric = trial.suggest_categorical('metric', KNN_METRICS)
    use_distance_weighting = trial.suggest_categorical('use_distance_weighting', [True, False])
    
    # Feature weights (her özellik için ayrı ağırlık)
    feature_weights = {}
    for feat in available_features:
        feature_weights[feat] = trial.suggest_float(f'weight_{feat}', 0.1, 2.0)
    
    # K-Fold CV
    kf = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
    cv_maes = []
    
    for train_idx, val_idx in kf.split(df_train_filtered):
        df_train_fold = df_train_filtered.iloc[train_idx]
        df_val_fold = df_train_filtered.iloc[val_idx]
        
        X_train_fold = df_train_fold[available_features].fillna(0)
        y_train_fold = df_train_fold[target_col]
        X_val_fold = df_val_fold[available_features].fillna(0)
        y_val_fold = df_val_fold[target_col]
        
        # Her validation örneği için tahmin yap
        predictions = []
        for idx in range(len(X_val_fold)):
            X_val_single = X_val_fold.iloc[[idx]]
            stats = predict_knn(
                X_train_fold, y_train_fold, X_val_single,
                k=k, metric=metric, feature_weights=feature_weights,
                use_distance_weighting=use_distance_weighting
            )
            predictions.append(stats['tahmin'])
        
        # MAE hesapla
        mae = mean_absolute_error(y_val_fold, predictions)
        cv_maes.append(mae)
    
    return np.mean(cv_maes)


def optimize_knn_hyperparameters(df_train, target_col, bin_idx=None, 
                                 n_trials=OPTUNA_N_TRIALS, cv_folds=CV_FOLDS):
    """
    KNN için Optuna hiperparametre optimizasyonu
    
    Args:
        df_train: Eğitim verisi DataFrame
        target_col: Hedef değişken adı
        bin_idx: Bin numarası (filtreleme için)
        n_trials: Optuna deneme sayısı
        cv_folds: CV fold sayısı
    
    Returns:
        best_params, best_cv_mae
    """
    study = optuna.create_study(
        direction='minimize',
        sampler=TPESampler(seed=42),
        study_name=f'knn_optimization_bin{bin_idx if bin_idx else "all"}'
    )
    
    study.optimize(
        lambda trial: objective_knn_cv(trial, df_train, target_col, bin_idx, cv_folds),
        n_trials=n_trials,
        timeout=OPTUNA_TIMEOUT,
        show_progress_bar=True
    )
    
    return study.best_params, study.best_value


class KNNOptunaModel:
    """
    KNN Model with Optuna Hyperparameter Optimization
    """
    
    def __init__(self):
        self.knn_params = {}  # Bin bazlı KNN parametreleri
        self.df_train = None  # Eğitim verisi
        self.bin_metrics = {}  # Bin bazlı metrikler
        self.available_features = []  # KNN için kullanılacak özellikler
    
    def train(self, df, target_col=TARGET_COL, test_size=0.2, n_trials=OPTUNA_N_TRIALS):
        """
        KNN model eğitimi
        
        Args:
            df: Eğitim verisi DataFrame
            target_col: Hedef değişken adı
            test_size: Test seti oranı
            n_trials: Optuna deneme sayısı
        """
        print("\n" + "="*80)
        print("KNN MODEL + OPTUNA HİPERPARAMETRE OPTİMİZASYONU")
        print("="*80)
        
        # Veri hazırlama
        df = df.dropna(how="all").copy()
        
        if target_col not in df.columns:
            raise ValueError(f"Hedef sütun bulunamadı: {target_col}")
        
        # Numeric dönüşümler
        for col in NUMERIC_CANDIDATES:
            if col in df.columns:
                df[col] = to_numeric_tr(df[col])
        
        # Boolean sütunlar
        for col in BOOLEAN_COLUMNS:
            if col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                elif df[col].dtype in ['float64', 'float32']:
                    df[col] = df[col].fillna(0).astype(int)
        
        # Target
        df[target_col] = to_numeric_tr(df[target_col])
        df = df[df[target_col].notna()].copy()
        
        # Feature engineering
        df = engineer_features(df)
        
        # Drop features
        drop_now = [c for c in DROP_FEATURES if c in df.columns]
        if drop_now:
            df.drop(columns=drop_now, inplace=True)
        
        # Inf temizliği
        df = df.replace([np.inf, -np.inf], np.nan)
        
        # Numeric NaN -> 0
        num_cols = df.select_dtypes(include=[np.number]).columns
        df[num_cols] = df[num_cols].fillna(0)
        
        # Train/Val split
        if "rayic_bedel" in df.columns:
            df["rayic_bin_4"] = df["rayic_bedel"].apply(get_rayic_bin_label)
            strata = df["rayic_bin_4"]
        else:
            strata = None
        
        df_train, df_val = train_test_split(
            df, test_size=test_size, random_state=42, stratify=strata
        )
        
        print(f"\n[INFO] Eğitim seti: {len(df_train):,} satır")
        print(f"[INFO] Validation seti: {len(df_val):,} satır")
        
        # KNN için kullanılacak özellikleri belirle
        self.available_features = []
        for feat in KNN_FEATURES:
            if feat in df_train.columns:
                self.available_features.append(feat)
            elif feat == "arac_kilometresi" and "arac_kilometresi" not in df_train.columns:
                if "km_k" in df_train.columns:
                    self.available_features.append("km_k")
        
        print(f"[INFO] KNN özellikleri: {self.available_features}")
        
        # Eğitim verisini sakla
        self.df_train = df_train.copy()
        
        # Bin bazlı model eğitimi
        print(f"\n[INFO] Bin bazlı KNN model eğitimi başlıyor...")
        overall_metrics = {'mae': [], 'rmse': [], 'r2': []}
        
        for bin_idx in range(1, 5):
            bin_name = f"bin{bin_idx}"
            print(f"\n{'='*60}")
            print(f"[INFO] {bin_name.upper()} KNN MODEL EĞİTİMİ + OPTUNA")
            print(f"{'='*60}")
            
            # Bin filtreleme
            if "rayic_bedel" in df_train.columns:
                min_val, max_val = RAYIC_BIN_BOUNDARIES[bin_idx - 1]
                if min_val == float('-inf'):
                    mask_train = df_train["rayic_bedel"] <= max_val
                    mask_val = df_val["rayic_bedel"] <= max_val
                elif max_val == float('inf'):
                    mask_train = df_train["rayic_bedel"] > min_val
                    mask_val = df_val["rayic_bedel"] > min_val
                else:
                    mask_train = (df_train["rayic_bedel"] > min_val) & (df_train["rayic_bedel"] <= max_val)
                    mask_val = (df_val["rayic_bedel"] > min_val) & (df_val["rayic_bedel"] <= max_val)
            else:
                mask_train = pd.Series([True] * len(df_train))
                mask_val = pd.Series([True] * len(df_val))
            
            df_bin_train = df_train[mask_train].copy()
            df_bin_val = df_val[mask_val].copy()
            
            if len(df_bin_train) == 0:
                print(f"[WARNING] {bin_name} için eğitim verisi yok, atlanıyor")
                continue
            
            print(f"[INFO] {bin_name} train: {len(df_bin_train):,} satır")
            print(f"[INFO] {bin_name} val: {len(df_bin_val):,} satır")
            
            # Optuna optimizasyonu
            print(f"[INFO] {bin_name} için Optuna optimizasyonu başlıyor...")
            best_params, best_cv_mae = optimize_knn_hyperparameters(
                df_bin_train, target_col, bin_idx=bin_idx, n_trials=n_trials, cv_folds=CV_FOLDS
            )
            print(f"[INFO] {bin_name} en iyi CV MAE: {best_cv_mae:,.2f} TL")
            print(f"[INFO] {bin_name} en iyi parametreler: {best_params}")
            
            # Parametreleri kaydet
            self.knn_params[bin_idx] = best_params
            
            # Validation performansı
            X_val = df_bin_val[self.available_features].fillna(0)
            y_val = df_bin_val[target_col]
            X_train = df_bin_train[self.available_features].fillna(0)
            y_train = df_bin_train[target_col]
            
            # Feature weights
            feature_weights = {}
            for feat in self.available_features:
                weight_key = f'weight_{feat}'
                if weight_key in best_params:
                    feature_weights[feat] = best_params[weight_key]
                else:
                    feature_weights[feat] = 1.0
            
            # Validation tahminleri
            predictions = []
            for idx in range(len(X_val)):
                X_val_single = X_val.iloc[[idx]]
                stats = predict_knn(
                    X_train, y_train, X_val_single,
                    k=best_params['k'],
                    metric=best_params['metric'],
                    feature_weights=feature_weights,
                    use_distance_weighting=best_params['use_distance_weighting']
                )
                predictions.append(stats['tahmin'])
            
            val_mae = mean_absolute_error(y_val, predictions)
            val_rmse = np.sqrt(mean_squared_error(y_val, predictions))
            val_r2 = r2_score(y_val, predictions)
            
            self.bin_metrics[bin_idx] = {
                'mae': val_mae,
                'rmse': val_rmse,
                'r2': val_r2,
                'cv_mae': best_cv_mae
            }
            
            overall_metrics['mae'].append(val_mae)
            overall_metrics['rmse'].append(val_rmse)
            overall_metrics['r2'].append(val_r2)
            
            print(f"[INFO] {bin_name} Validation MAE: {val_mae:,.2f} TL")
            print(f"[INFO] {bin_name} Validation RMSE: {val_rmse:,.2f} TL")
            print(f"[INFO] {bin_name} Validation R²: {val_r2:.4f}")
        
        # Genel metrikler
        print("\n" + "="*80)
        print("📊 GENEL PERFORMANS METRİKLERİ")
        print("="*80)
        if overall_metrics['mae']:
            print(f"Ortalama MAE: {np.mean(overall_metrics['mae']):,.2f} TL")
            print(f"Ortalama RMSE: {np.mean(overall_metrics['rmse']):,.2f} TL")
            print(f"Ortalama R²: {np.mean(overall_metrics['r2']):.4f}")
        
        print("\n" + "="*80)
        print("✅ MODEL EĞİTİMİ TAMAMLANDI")
        print("="*80)
    
    def predict(self, df_input, target_col=TARGET_COL):
        """
        KNN tahmin yapma
        
        Args:
            df_input: Tahmin yapılacak veri DataFrame (tek satır)
            target_col: Hedef değişken adı
        
        Returns:
            dict: Tahmin sonuçları
        """
        results = {
            'tahmin': 0,
            'min': 0,
            'max': 0,
            'median': 0,
            'confidence': 0.0,
            'bin_idx': 1
        }
        
        if self.df_train is None or len(self.knn_params) == 0:
            print("[ERROR] Model eğitilmemiş!")
            return results
        
        # Veri hazırlama
        df_input_processed = df_input.copy()
        
        # Numeric dönüşümler
        for col in NUMERIC_CANDIDATES:
            if col in df_input_processed.columns:
                df_input_processed[col] = to_numeric_tr(df_input_processed[col])
        
        # Boolean sütunlar
        for col in BOOLEAN_COLUMNS:
            if col in df_input_processed.columns:
                if df_input_processed[col].dtype == 'object':
                    df_input_processed[col] = pd.to_numeric(df_input_processed[col], errors='coerce').fillna(0).astype(int)
        
        # Feature engineering
        df_input_processed = engineer_features(df_input_processed)
        
        # Inf temizliği
        df_input_processed = df_input_processed.replace([np.inf, -np.inf], np.nan)
        
        # Numeric NaN -> 0
        num_cols = df_input_processed.select_dtypes(include=[np.number]).columns
        df_input_processed[num_cols] = df_input_processed[num_cols].fillna(0)
        
        # Bin belirleme
        if "rayic_bedel" in df_input_processed.columns:
            rayic_val = df_input_processed["rayic_bedel"].iloc[0] if len(df_input_processed) > 0 else 0
            try:
                rayic_val = float(rayic_val) if not pd.isna(rayic_val) else 0
            except:
                rayic_val = 0
            bin_idx = get_rayic_bin_idx(rayic_val)
        else:
            bin_idx = 1
            rayic_val = 0
        
        results['bin_idx'] = bin_idx
        
        # Bin için parametreleri al
        if bin_idx not in self.knn_params:
            # Fallback: en yakın bin'i kullan veya tüm veriyi kullan
            bin_idx = min(self.knn_params.keys(), key=lambda x: abs(x - bin_idx))
        
        params = self.knn_params[bin_idx]
        
        # Eğitim verisini hazırla
        X_train = self.df_train[self.available_features].fillna(0)
        y_train = self.df_train[target_col] if target_col in self.df_train.columns else self.df_train[TARGET_COL]
        X_input = df_input_processed[self.available_features].fillna(0)
        
        # Feature weights
        feature_weights = {}
        for feat in self.available_features:
            weight_key = f'weight_{feat}'
            if weight_key in params:
                feature_weights[feat] = params[weight_key]
            else:
                feature_weights[feat] = 1.0
        
        # Tahmin yap
        stats = predict_knn(
            X_train, y_train, X_input,
            k=params['k'],
            metric=params['metric'],
            feature_weights=feature_weights,
            use_distance_weighting=params['use_distance_weighting'],
            bin_idx=bin_idx
        )
        
        results.update(stats)
        
        return results
    
    def save_model(self, filepath="knn_optuna_model.pkl"):
        """Modeli kaydet"""
        model_data = {
            'knn_params': self.knn_params,
            'df_train': self.df_train,
            'bin_metrics': self.bin_metrics,
            'available_features': self.available_features
        }
        
        joblib.dump(model_data, filepath)
        print(f"💾 Model kaydedildi: {filepath}")
    
    def load_model(self, filepath="knn_optuna_model.pkl"):
        """Modeli yükle"""
        model_data = joblib.load(filepath)
        self.knn_params = model_data['knn_params']
        self.df_train = model_data['df_train']
        self.bin_metrics = model_data.get('bin_metrics', {})
        self.available_features = model_data.get('available_features', [])
        print(f"✅ Model yüklendi: {filepath}")


def main():
    """Ana eğitim fonksiyonu"""
    # Script'in bulunduğu klasörü bul
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, EXCEL_PATH)
    
    # Eğer script klasöründe yoksa, karma klasöründe ara
    if not os.path.exists(excel_path):
        karma_path = os.path.join(os.path.dirname(script_dir), "karma", EXCEL_PATH)
        if os.path.exists(karma_path):
            excel_path = karma_path
        else:
            # Ana dizinde ara
            root_path = os.path.join(os.path.dirname(script_dir), EXCEL_PATH)
            if os.path.exists(root_path):
                excel_path = root_path
    
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel bulunamadı: {EXCEL_PATH}\nAranan konumlar:\n  - {os.path.join(script_dir, EXCEL_PATH)}\n  - {os.path.join(os.path.dirname(script_dir), 'karma', EXCEL_PATH)}\n  - {os.path.join(os.path.dirname(script_dir), EXCEL_PATH)}")
    
    print("\n" + "="*80)
    print("KNN MODEL + OPTUNA HİPERPARAMETRE OPTİMİZASYONU")
    print("="*80)
    print(f"📂 Excel dosyası: {excel_path}")
    
    # Veri yükle
    df = pd.read_excel(excel_path)
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]
    
    # Model oluştur ve eğit
    model = KNNOptunaModel()
    model.train(df, n_trials=OPTUNA_N_TRIALS)
    
    # Modeli karma klasörüne kaydet
    # Script'in bulunduğu klasörü kontrol et
    if os.path.basename(script_dir) == "karma":
        # Script zaten karma klasöründe
        karma_dir = script_dir
    else:
        # Karma klasörünü bul
        karma_dir = os.path.join(os.path.dirname(script_dir), "karma")
        if not os.path.exists(karma_dir):
            # Karma klasörü yoksa, script'in bulunduğu yerde oluştur
            karma_dir = script_dir
    
    model_path = os.path.join(karma_dir, "knn_optuna_model.pkl")
    model.save_model(model_path)
    
    print("\n" + "="*80)
    print("✅ EĞİTİM TAMAMLANDI!")
    print("="*80)
    
    return model


if __name__ == "__main__":
    model = main()
