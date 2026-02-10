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
        # Bulunamazsa default kullan
        try:
            return PARCA_KATSAYI_TABLOSU["default"][islem_turu][hasar_seviyesi]
        except Exception:
            return 0.75  # Son çare: ortalama katsayı
# Parça/işlem/hasar katsayı tablosu (Devlet belgesi tablolarından)
# Format: {"PARCA_KODU": {"degisim": {"hafif": katsayi, "orta": katsayi, "yuksek": katsayi}, "onarim": {"hafif": katsayi, ...}}}
PARCA_KATSAYI_TABLOSU = {
    # Otomobil parçaları (A serisi)
    "A.1": {  # TAVAN SACI
        "degisim": {"hafif": 1.80, "orta": 2.00, "yuksek": 2.00},
        "onarim": {"hafif": 1.30, "orta": 1.50, "yuksek": 1.80},
    },
    "A.2": {  # ÖN PANEL (SAÇ)
        "degisim": {"hafif": 1.50, "orta": 1.80, "yuksek": 2.00},
        "onarim": {"hafif": 1.00, "orta": 1.20, "yuksek": 1.50},
    },
    "A.3": {  # SAĞ ÖN ÇAMURLUK (SAÇ)
        "degisim": {"hafif": 0.80, "orta": 1.00, "yuksek": 1.20},
        "onarim": {"hafif": 0.60, "orta": 0.80, "yuksek": 1.00},
    },
    "A.4": {  # SOL ÖN ÇAMURLUK (SAÇ)
        "degisim": {"hafif": 0.80, "orta": 1.00, "yuksek": 1.20},
        "onarim": {"hafif": 0.60, "orta": 0.80, "yuksek": 1.00},
    },
    "A.10": {  # MOTOR KAPUTU
        "degisim": {"hafif": 0.60, "orta": 0.80, "yuksek": 1.00},
        "onarim": {"hafif": 0.50, "orta": 0.75, "yuksek": 0.90},
    },
    "A.11": {  # SAĞ ÖN KAPI (KAPI SACI)
        "degisim": {"hafif": 0.60, "orta": 0.80, "yuksek": 1.00},
        "onarim": {"hafif": 0.40, "orta": 0.60, "yuksek": 0.80},
    },
    "A.12": {  # SOL ÖN KAPI (KAPI SACI)
        "degisim": {"hafif": 0.60, "orta": 0.80, "yuksek": 1.00},
        "onarim": {"hafif": 0.40, "orta": 0.60, "yuksek": 0.80},
    },
    "A.13": {  # SAĞ ARKA KAPI (KAPI SACI)
        "degisim": {"hafif": 0.60, "orta": 0.80, "yuksek": 1.00},
        "onarim": {"hafif": 0.40, "orta": 0.60, "yuksek": 0.80},
    },
    "A.14": {  # SOL ARKA KAPI (KAPI SACI)
        "degisim": {"hafif": 0.60, "orta": 0.80, "yuksek": 1.00},
        "onarim": {"hafif": 0.40, "orta": 0.60, "yuksek": 0.80},
    },
    "A.21": {  # BAGAJ KAPAĞI
        "degisim": {"hafif": 0.60, "orta": 0.80, "yuksek": 1.00},
        "onarim": {"hafif": 0.50, "orta": 0.70, "yuksek": 0.90},
    },
    "A.23": {  # SAĞ ARKA ÇAMURLUK
        "degisim": {"hafif": 0.80, "orta": 1.00, "yuksek": 1.20},
        "onarim": {"hafif": 0.60, "orta": 1.00, "yuksek": 1.20},
    },
    "A.24": {  # SOL ARKA ÇAMURLUK
        "degisim": {"hafif": 0.80, "orta": 1.00, "yuksek": 1.20},
        "onarim": {"hafif": 0.60, "orta": 1.00, "yuksek": 1.20},
    },
    # Default katsayılar (bulunamayanlar için)
    "default": {
        "degisim": {"hafif": 0.80, "orta": 1.00, "yuksek": 1.20},
        "onarim": {"hafif": 0.50, "orta": 0.75, "yuksek": 1.00},
    },
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


# ============================================================================
# DEVLET KATSAYILARı (2018 Sayılı Karayolları Trafik Kanunu - EK1)
# ============================================================================

def get_rayic_katsayisi(rayic_bedel, arac_grubu="A"):
    """Devlet tablosuna göre Rayiç Değer Katsayısı (R)"""
    if pd.isna(rayic_bedel):
        return 0.65
    
    rayic = float(rayic_bedel)
    
    # Tablo R.1 (A, D) - Otomobil, İş makinesi, Traktör, Tarım makinesi, Tanker
    if arac_grubu in ["A", "D"]:
        if rayic <= 39999:
            return 0.65
        elif rayic <= 99999:
            return 0.70
        elif rayic <= 199999:
            return 0.75
        elif rayic <= 299999:
            return 0.80
        elif rayic <= 399999:
            return 0.85
        elif rayic <= 499999:
            return 0.90
        elif rayic <= 749999:
            return 0.95
        else:
            return 1.00
    
    # Tablo R.2 (B, C, Ç, E) - Minibüs, Otobüs, Kamyonet, Kamyon, Çekici, Römork, Motorsiklet
    else:
        if rayic <= 249999:
            return 0.65
        elif rayic <= 349999:
            return 0.70
        elif rayic <= 499999:
            return 0.75
        elif rayic <= 749999:
            return 0.80
        elif rayic <= 999999:
            return 0.85
        elif rayic <= 1249999:
            return 0.90
        elif rayic <= 1499999:
            return 0.95
        else:
            return 1.00


def get_kilometre_katsayisi(kilometre, arac_grubu="A"):
    """Devlet tablosuna göre Kilometre Katsayısı (K)"""
    if pd.isna(kilometre):
        return 1.00
    
    km = float(kilometre)
    
    # Tablo K.1 (A, F) - Otomobil, Motorsiklet, Özel amaçlı araç, Tanker
    if arac_grubu in ["A", "F", "Ç"]:
        if km < 20000:
            return 1.00
        elif km < 50000:
            return 0.95
        elif km < 100000:
            return 0.90
        elif km < 150000:
            return 0.85
        elif km < 200000:
            return 0.80
        elif km < 300000:
            return 0.75
        else:
            return 0.70
    
    # Tablo K.2 (B, C, Ç, E) - Minibüs, Otobüs, Kamyonet, Kamyon, Çekici, Römork
    elif arac_grubu in ["B", "C", "E"]:
        if km < 50000:
            return 1.00
        elif km < 150000:
            return 0.95
        elif km < 300000:
            return 0.90
        elif km < 500000:
            return 0.85
        elif km < 750000:
            return 0.80
        elif km < 1000000:
            return 0.75
        else:
            return 0.70
    
    # Tablo K.3 (D) - İş makinesi, Traktör (çalışma saati bazlı, ama km olarak da geçebilir)
    else:
        if km < 500:
            return 1.00
        elif km < 1000:
            return 0.95
        elif km < 2000:
            return 0.90
        elif km < 3000:
            return 0.85
        elif km < 4000:
            return 0.80
        elif km < 5000:
            return 0.75
        else:
            return 0.70


def get_hasar_katsayisi_basit(degisen_parca_sayisi, onarilan_parca_sayisi):
    """Basitleştirilmiş Hasar Katsayısı (H) - parça sayılarına göre ortalama"""
    degisen = float(degisen_parca_sayisi) if not pd.isna(degisen_parca_sayisi) else 0
    onarilan = float(onarilan_parca_sayisi) if not pd.isna(onarilan_parca_sayisi) else 0
    
    # Toplam hasar katsayısı: Değişen tam, onarılan yarım ağırlık
    total_hasar = (degisen * 1.0) + (onarilan * 0.5)
    
    # Makul bir aralıkta tutmak için cap koy (max 10)
    if total_hasar > 10:
        total_hasar = 10
    
    # Minimum 0.5 (en az bir parça varsa)
    if total_hasar < 0.5 and (degisen > 0 or onarilan > 0):
        total_hasar = 0.5
    
    return total_hasar


def get_hasar_katsayisi_detayli(parca_katsayilari_list):
    """Detaylı Hasar Katsayısı (H) - gerçek parça katsayılarına göre
    
    Args:
        parca_katsayilari_list: Liste of dict with keys: parca_kodu, islem_turu, hasar_seviyesi
    
    Returns:
        float: Toplam hasar katsayısı (parça katsayılarının toplamı)
    """
    if not parca_katsayilari_list or len(parca_katsayilari_list) == 0:
        return 0.5  # Minimum katsayı
    
    total_katsayi = 0.0
    
    for parca_dict in parca_katsayilari_list:
        parca_kodu = parca_dict.get('parca_kodu', '')
        islem_turu = parca_dict.get('islem_turu', 'onarim')
        hasar_seviyesi = parca_dict.get('hasar_seviyesi', 'orta')
        
        # get_parca_katsayi fonksiyonunu kullan
        katsayi = get_parca_katsayi(parca_kodu, islem_turu, hasar_seviyesi)
        total_katsayi += katsayi
    
    # Makul bir aralıkta tutmak için cap koy (max 10)
    if total_katsayi > 10:
        total_katsayi = 10
    
    # Minimum 0.5
    if total_katsayi < 0.5:
        total_katsayi = 0.5
    
    return total_katsayi


def get_marka_model_carpan(marka, model):
    """Marka/model segmentine göre çarpan (0.90-1.10 arası, çok küçük etki)"""
    if pd.isna(marka):
        return 1.0
    
    marka_str = str(marka).lower().strip()
    model_str = str(model).lower().strip() if not pd.isna(model) else ""
    
    # Lüks araçlar: %8 daha fazla değer kaybı
    luks_markalar = ["mercedes", "bmw", "audi", "porsche", "tesla", "jaguar", "land rover", 
                     "lexus", "infiniti", "maserati", "ferrari", "lamborghini", "bentley", 
                     "rolls-royce", "aston martin", "alpine", "lotus"]
    for luks in luks_markalar:
        if luks in marka_str:
            return 1.08
    
    # Düşük segment: %8 daha az değer kaybı
    dusuk_markalar = ["tofaş", "tofas", "lada", "proton"]
    for dusuk in dusuk_markalar:
        if dusuk in marka_str:
            return 0.92
    
    # Ticari/Minibüs/Otobüs modelleri: %3 daha az (çalışma aracı)
    ticari_modeller = ["doblo", "transit", "transporter", "sprinter", "jumpy", "boxer", 
                       "vivaro", "caddy", "kangoo", "ducato", "master", "daily", "minibüs", 
                       "minibus", "otobüs", "otobus", "kamyonet"]
    for ticari in ticari_modeller:
        if ticari in model_str:
            return 0.97
    
    # Orta segment: nötr
    return 1.0


def get_arac_yasi_carpan(arac_yasi):
    """Araç yaşı kategorisine göre çarpan (0.97-1.03 arası, çok küçük etki)"""
    if pd.isna(arac_yasi):
        return 1.0
    
    yas = float(arac_yasi)
    
    # 0-5 yaş: Yeni araçta değer kaybı biraz daha fazla (itibar kaybı)
    if yas <= 5:
        return 1.02
    # 5-10 yaş: Orta, nötr
    elif yas <= 10:
        return 1.0
    # 10-15 yaş: Biraz daha az
    elif yas <= 15:
        return 0.99
    # 15-20 yaş: Daha az
    elif yas <= 20:
        return 0.98
    # 20+ yaş: En az (eski araçta değer kaybı zaten düşük)
    else:
        return 0.97


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
        
        # ============================================================================
        # HİBRİD MODEL: KNN BASELINE + DEVLET KATSAYILARı
        # ============================================================================
        # KNN'den gelen tahmin (baseline)
        knn_baseline = results['tahmin']
        
        # Input verilerini al
        row = df_input_processed.iloc[0]
        
        # Araç grubunu belirle (minibüs/otobüs/ticari için farklı tablolar)
        arac_grubu = "A"  # Default: Otomobil
        if "marka" in row and not pd.isna(row["marka"]):
            marka_lower = str(row["marka"]).lower()
            model_lower = str(row.get("model", "")).lower() if "model" in row else ""
            
            # Ticari araç tespiti
            ticari_keywords = ["kamyonet", "kamyon", "çekici", "tanker", "iş makinesi", 
                              "traktör", "römork", "transit", "sprinter", "daily", "boxer", 
                              "ducato", "master", "jumpy"]
            if any(kw in marka_lower or kw in model_lower for kw in ticari_keywords):
                arac_grubu = "C"  # Ticari
            
            # Minibüs/Otobüs tespiti
            minibus_keywords = ["minibüs", "minibus", "otobüs", "otobus", "midibüs", "midibus"]
            if any(kw in marka_lower or kw in model_lower for kw in minibus_keywords):
                arac_grubu = "B"  # Minibüs/Otobüs
        
        # Devlet katsayılarını hesapla
        R = get_rayic_katsayisi(row.get("rayic_bedel", rayic_val), arac_grubu)
        K = get_kilometre_katsayisi(row.get("arac_kilometresi", 0), arac_grubu)
        
        # Hasar katsayısı: parca_katsayilari varsa detaylı, yoksa basit
        if "parca_katsayilari" in row:
            parca_list = row["parca_katsayilari"]
            # parca_list bir liste dict olmalı ve boş olmamalı
            if isinstance(parca_list, list) and len(parca_list) > 0:
                H_raw = get_hasar_katsayisi_detayli(parca_list)
            else:
                H_raw = get_hasar_katsayisi_basit(
                    row.get("degisen_parca_sayisi", 0),
                    row.get("onarilan_parca_sayisi", 0)
                )
        else:
            H_raw = get_hasar_katsayisi_basit(
                row.get("degisen_parca_sayisi", 0),
                row.get("onarilan_parca_sayisi", 0)
            )
        
        # H normalize et (çarpımsal patlamayı önle)
        H = 1.0 + (H_raw / 10.0)  # Örnek: 5 parça → 1.5x
        
        # Marka/model ve yaş çarpanları (çok küçük etkiler)
        marka_carpan = get_marka_model_carpan(
            row.get("marka", ""),
            row.get("model", "")
        )
        yas_carpan = get_arac_yasi_carpan(row.get("arac_yasi", 0))
        
        # HİBRİD FORMÜL: KNN baseline × Devlet katsayıları × Marka/Yaş çarpanları
        adjusted_pred = knn_baseline * R * K * H * marka_carpan * yas_carpan
        
        # Negatif değerleri ve aşırı sonuçları engelle
        if adjusted_pred < 0:
            adjusted_pred = 0
        
        # Sonuçları güncelle
        results['tahmin'] = adjusted_pred
        results['knn_baseline'] = knn_baseline
        results['katsayi_R_rayic'] = R
        results['katsayi_K_kilometre'] = K
        results['katsayi_H_hasar'] = H
        results['carpan_marka_model'] = marka_carpan
        results['carpan_arac_yasi'] = yas_carpan
        results['carpim'] = R * K * H * marka_carpan * yas_carpan
        
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
