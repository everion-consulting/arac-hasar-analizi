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

