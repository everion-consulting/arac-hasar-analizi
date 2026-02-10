"""Parça katsayılarının test edilmesi"""
import pandas as pd
from backend.knn_optuna_model import KNNOptunaModel

# Model yükle
model = KNNOptunaModel()
model.load_model('backend/knn_optuna_model.pkl')

# Test senaryoları - AYNI PARAMETRELERİ GİR, SADECE PARÇAYI DEĞİŞTİR
base_data = {
    "rayic_bedel": 500000,
    "hasar_bedeli": 50000,
    "degisen_parca_sayisi": 0,
    "onarilan_parca_sayisi": 1,  # 1 parça onarıldı
    "arac_kilometresi": 50000,
    "marka": "Mercedes",
    "model": "C180",
    "arac_yasi": 5
}

test_cases = [
    {
        **base_data,
        "name": "Motor Kaputu (Onarım, Orta) - Katsayı: 0.75",
        "parca_katsayilari": [
            {
                "parca_kodu": "A.10",  # MOTOR KAPUTU
                "islem_turu": "onarim",
                "hasar_seviyesi": "orta"
            }
        ]
    },
    {
        **base_data,
        "name": "Sağ Arka Çamurluk (Onarım, Orta) - Katsayı: 1.00",
        "parca_katsayilari": [
            {
                "parca_kodu": "A.23",  # SAĞ ARKA ÇAMURLUK
                "islem_turu": "onarim",
                "hasar_seviyesi": "orta"
            }
        ]
    },
    {
        **base_data,
        "name": "Sağ Ön Kapı (Onarım, Orta) - Katsayı: 0.60",
        "parca_katsayilari": [
            {
                "parca_kodu": "A.11",  # SAĞ ÖN KAPI
                "islem_turu": "onarim",
                "hasar_seviyesi": "orta"
            }
        ]
    }
]

print("\n" + "="*100)
print("PARÇA KATSAYISI TEST SONUÇLARI")
print("="*100)
print("\n⚠️  BEKLENTİ: Motor kaputu (0.75) < Sağ ön kapı (0.60) < Çamurluk (1.00)")
print("="*100)

for i, test in enumerate(test_cases, 1):
    print(f"\n📋 Test {i}: {test['name']}")
    print("-" * 100)
    
    # DataFrame oluştur
    df_test = pd.DataFrame([test])
    
    # Tahmin yap
    result = model.predict(df_test)
    
    # Sonuçları göster
    print(f"  ⚙️  KNN Baseline: {result.get('knn_baseline', 0):,.2f} TL")
    print(f"  📊 Katsayı H (Hasar): {result.get('katsayi_H_hasar', 1.0):.4f}")
    print(f"  ✅ SONUÇ TAHMİN: {result.get('tahmin', 0):,.2f} TL")

print("\n" + "="*100)
print("📌 SONUÇ ANALİZİ:")
print("   - Motor kaputu (0.75) → En düşük tahmin olmalı")
print("   - Sağ ön kapı (0.60) → Orta tahmin")
print("   - Çamurluk (1.00) → En yüksek tahmin olmalı")
print("="*100 + "\n")
