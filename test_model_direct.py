"""Model direkt test - API bypass"""
import pandas as pd
from backend.knn_optuna_model import KNNOptunaModel

# Model yükle
model = KNNOptunaModel()
model.load_model('backend/knn_optuna_model.pkl')

# Test 1: Motor Kaputu
test1_data = {
    "rayic_bedel": 500000,
    "hasar_bedeli": 50000,
    "degisen_parca_sayisi": 0,
    "onarilan_parca_sayisi": 1,
    "arac_kilometresi": 50000,
    "marka": "Mercedes",
    "model": "C180",
    "arac_yasi": 5,
    "parca_katsayilari": [
        {
            "parca_kodu": "A.10",
            "islem_turu": "onarim",
            "hasar_seviyesi": "orta"
        }
    ]
}

# Test 2: Çamurluk
test2_data = {
    "rayic_bedel": 500000,
    "hasar_bedeli": 50000,
    "degisen_parca_sayisi": 0,
    "onarilan_parca_sayisi": 1,
    "arac_kilometresi": 50000,
    "marka": "Mercedes",
    "model": "C180",
    "arac_yasi": 5,
    "parca_katsayilari": [
        {
            "parca_kodu": "A.23",
            "islem_turu": "onarim",
            "hasar_seviyesi": "orta"
        }
    ]
}

print("\n" + "="*80)
print("MODEL DİREKT TEST (API BYPASS)")
print("="*80)

print("\n📋 Test 1: Motor Kaputu (A.10 - Onarım Orta: 0.75)")
df1 = pd.DataFrame([test1_data])
result1 = model.predict(df1)
print(f"   KNN Baseline: {result1.get('knn_baseline', 0):,.2f} TL")
print(f"   Katsayı H: {result1.get('katsayi_H_hasar', 1.0):.4f}")
print(f"   Sonuç: {result1.get('tahmin', 0):,.2f} TL")

print("\n📋 Test 2: Çamurluk (A.23 - Onarım Orta: 1.00)")
df2 = pd.DataFrame([test2_data])
result2 = model.predict(df2)
print(f"   KNN Baseline: {result2.get('knn_baseline', 0):,.2f} TL")
print(f"   Katsayı H: {result2.get('katsayi_H_hasar', 1.0):.4f}")
print(f"   Sonuç: {result2.get('tahmin', 0):,.2f} TL")

print("\n" + "="*80)
if abs(result1.get('tahmin', 0) - result2.get('tahmin', 0)) > 1:
    print("✅ BAŞARILI: Farklı sonuçlar!")
else:
    print("❌ BAŞARISIZ: Aynı sonuç!")
print("="*80 + "\n")
