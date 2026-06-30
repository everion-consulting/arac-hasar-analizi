import os
import sys
from pathlib import Path

from django.conf import settings

# FastAPI tarafındaki `backend/knn_optuna_model.py` dosyasını kullanmak için
# o klasörü Python path'ine ekliyoruz.
PROJECT_ROOT = settings.BASE_DIR.parent  # .../arac-hasar-analizi/
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from knn_optuna_model import KNNOptunaModel  # type: ignore


# Model dosyasının yolu (FastAPI backend'inde kullanılan yapıya paralel)
MODEL_PATH = os.path.join(
    BACKEND_DIR,
    "knn_optuna_model.pkl",
)


# Global (lazy-load) model nesnesi
_knn_model = None


def get_knn_model() -> KNNOptunaModel:
    """
    KNNOptunaModel örneğini tekil (singleton) olarak döndürür.
    İlk çağrıda .pkl dosyasını yükler, sonrasında aynı nesneyi tekrar kullanır.
    """
    global _knn_model
    if _knn_model is None:
        model = KNNOptunaModel()
        model.load_model(MODEL_PATH)
        _knn_model = model
    return _knn_model


def _normalize_islem_turu(islem):
    if not isinstance(islem, str):
        return islem
    islem_lower = islem.lower()
    if "degisim" in islem_lower:
        return "degisim"
    if "onarim" in islem_lower:
        return "onarim"
    return islem_lower


def _prepare_predict_data(data: dict) -> dict:
    data = dict(data)
    for key in ["degisen_aciklama", "onarilan_aciklama", "marka", "model"]:
        value = data.get(key)
        if isinstance(value, str):
            data[key] = value.strip().lower()

    parca_katsayilari = []
    for p in data.get("degisen_parcalar", []) or []:
        parca_katsayilari.append(
            {
                "parca_kodu": p.get("parca_kodu", ""),
                "islem_turu": _normalize_islem_turu(p.get("islemTuru", "degisim")),
                "hasar_seviyesi": p.get("seviye", "hafif") or "hafif",
            }
        )
    for p in data.get("onarilan_parcalar", []) or []:
        parca_katsayilari.append(
            {
                "parca_kodu": p.get("parca_kodu", ""),
                "islem_turu": _normalize_islem_turu(p.get("islemTuru", "onarim")),
                "hasar_seviyesi": p.get("seviye", "hafif") or "hafif",
            }
        )

    data["parca_katsayilari"] = parca_katsayilari
    return data


def execute_prediction(
    data: dict,
    *,
    user=None,
    frontend_user=None,
    save_to_db: bool = True,
) -> dict:
    """
    ML tahmini çalıştırır. save_to_db=True ise HasarTahmin kaydı oluşturur.
    """
    import pandas as pd

    from .models import HasarTahmin

    prepared = _prepare_predict_data(data)
    df = pd.DataFrame([prepared])
    model = get_knn_model()
    result = model.predict(df)

    if isinstance(result, dict):
        tahmini = float(result.get("tahmin", 0))
        uyari = result.get("uyari")
        katsayi_H_hasar = result.get("katsayi_H_hasar")
        knn_baseline = result.get("knn_baseline")
    else:
        tahmini = float(result[0]) if hasattr(result, "__getitem__") else float(result)
        uyari = None
        katsayi_H_hasar = None
        knn_baseline = None

    rayic_bedel = float(prepared.get("rayic_bedel", 0))
    min_val = max(0.0, tahmini - rayic_bedel * 0.005)
    max_val = max(0.0, tahmini + rayic_bedel * 0.005)

    response_data = {
        "min": round(min_val, 2),
        "max": round(max_val, 2),
        "tahmini": round(tahmini, 2),
        "uyari": uyari,
        "rayic_bedel": rayic_bedel,
        "katsayi_H_hasar": katsayi_H_hasar,
        "knn_baseline": knn_baseline,
    }

    if save_to_db:
        hasar = HasarTahmin.objects.create(
            user=user,
            frontend_user=frontend_user,
            rayic_bedel=prepared["rayic_bedel"],
            hasar_bedeli=prepared["hasar_bedeli"],
            degisen_parca_sayisi=prepared["degisen_parca_sayisi"],
            onarilan_parca_sayisi=prepared["onarilan_parca_sayisi"],
            arac_kilometresi=prepared["arac_kilometresi"],
            arac_yasi=prepared.get("arac_yasi") or 0,
            marka=prepared.get("marka"),
            model=prepared.get("model"),
            arac_turu=prepared.get("arac_turu"),
            arac_kodu=prepared.get("arac_kodu"),
            degisen_parcalar=prepared.get("degisen_parcalar"),
            onarilan_parcalar=prepared.get("onarilan_parcalar"),
            parca_katsayilari=prepared["parca_katsayilari"],
            tahmini=tahmini,
            min_deger=min_val,
            max_deger=max_val,
            uyari=uyari,
            katsayi_H_hasar=katsayi_H_hasar,
            knn_baseline=knn_baseline,
        )
        response_data["id"] = hasar.id

    return response_data

