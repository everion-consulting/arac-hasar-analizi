from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from backend.knn_optuna_model import KNNOptunaModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()
model = KNNOptunaModel()
model.load_model('knn_optuna_model.pkl')

app.mount("/", StaticFiles(directory="frontend_build", html=True), name="static")

class PredictRequest(BaseModel):
    rayic_bedel: float
    hasar_bedeli: float
    degisen_parca_sayisi: float
    onarilan_parca_sayisi: float
    arac_kilometresi: float
    degisen_parcalar: list = []
    onarilan_parcalar: list = []
    degisen_aciklama: str = ""
    onarilan_aciklama: str = ""
    marka: str = ""
    model: str = ""

@app.post('/predict')
async def predict(request: PredictRequest):
    data = request.dict()
    # String alanları normalize et
    for key in ['degisen_aciklama', 'onarilan_aciklama', 'marka', 'model']:
        if key in data and isinstance(data[key], str):
            data[key] = data[key].strip().lower()

    def normalize_islem_turu(islem):
        if 'degisim' in islem:
            return 'degisim'
        if 'onarim' in islem:
            return 'onarim'
        return islem

    parca_katsayilari = []
    for p in data.get('degisen_parcalar', []):
        parca_kodu = p.get('parca_kodu', '')
        islem_turu = normalize_islem_turu(p.get('islemTuru', 'degisim'))
        seviye = p.get('seviye', 'hafif') or 'hafif'
        parca_katsayilari.append({
            'parca_kodu': parca_kodu,
            'islem_turu': islem_turu,
            'hasar_seviyesi': seviye
        })
    for p in data.get('onarilan_parcalar', []):
        parca_kodu = p.get('parca_kodu', '')
        islem_turu = normalize_islem_turu(p.get('islemTuru', 'onarim'))
        seviye = p.get('seviye', 'hafif') or 'hafif'
        parca_katsayilari.append({
            'parca_kodu': parca_kodu,
            'islem_turu': islem_turu,
            'hasar_seviyesi': seviye
        })

    data['parca_katsayilari'] = parca_katsayilari
    df = pd.DataFrame([data])
    try:
        result = model.predict(df)
        if isinstance(result, dict):
            return {
                "min": round(result.get("min", 0), 2),
                "max": round(result.get("max", 0), 2),
                "tahmini": round(result.get("tahmin", 0), 2),
                "uyari": result.get("uyari"),
                "rayic_bedel": float(data.get("rayic_bedel", 0))
            }
        tahmini = float(result[0]) if hasattr(result, '__getitem__') else float(result)
        min_val = tahmini * 0.9
        max_val = tahmini * 1.1
        return {"min": round(min_val,2), "max": round(max_val,2), "tahmini": round(tahmini,2)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})