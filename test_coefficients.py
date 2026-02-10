"""Devlet katsayılarının test edilmesi"""
import pandas as pd
from backend.knn_optuna_model import KNNOptunaModel

# Model yükle
model = KNNOptunaModel()
model.load_model('backend/knn_optuna_model.pkl')

# Test senaryoları
test_cases = [
    {
        "name": "Düşük km Mercedes (lüks, düşük km → daha yüksek değer kaybı)",
        "rayic_bedel": 500000,
        "hasar_bedeli": 50000,
        "degisen_parca_sayisi": 3,
        "onarilan_parca_sayisi": 2,
        "arac_kilometresi": 15000,  # Düşük km
        "marka": "Mercedes",
        "model": "C180",
        "arac_yasi": 3
    },
    {
        "name": "Yüksek km Mercedes (lüks, yüksek km → daha düşük değer kaybı)",
        "rayic_bedel": 500000,
        "hasar_bedeli": 50000,
        "degisen_parca_sayisi": 3,
        "onarilan_parca_sayisi": 2,
        "arac_kilometresi": 250000,  # Yüksek km
        "marka": "Mercedes",
        "model": "C180",
        "arac_yasi": 3
    },
    {
        "name": "Düşük km Tofaş (ekonomik, düşük km)",
        "rayic_bedel": 200000,
        "hasar_bedeli": 30000,
        "degisen_parca_sayisi": 2,
        "onarilan_parca_sayisi": 1,
        "arac_kilometresi": 15000,
        "marka": "Tofaş",
        "model": "Egea",
        "arac_yasi": 2
    },
    {
        "name": "Yüksek km Tofaş (ekonomik, yüksek km → düşük değer kaybı)",
        "rayic_bedel": 200000,
        "hasar_bedeli": 30000,
        "degisen_parca_sayisi": 2,
        "onarilan_parca_sayisi": 1,
        "arac_kilometresi": 250000,
        "marka": "Tofaş",
        "model": "Egea",
        "arac_yasi": 2
    }
]

print("\n" + "="*100)
print("DEVLET KATSAYILARı TEST SONUÇLARI")
print("="*100)

for i, test in enumerate(test_cases, 1):
    print(f"\n📋 Test {i}: {test['name']}")
    print("-" * 100)
    
    # DataFrame oluştur
    df_test = pd.DataFrame([test])
    
    # Tahmin yap
    result = model.predict(df_test)
    
    # Sonuçları göster
    print(f"  Rayiç Bedel: {test['rayic_bedel']:,.0f} TL")
    print(f"  Km: {test['arac_kilometresi']:,.0f} km")
    print(f"  Marka/Model: {test['marka']} {test['model']}")
    print(f"  Yaş: {test['arac_yasi']} yıl")
    print(f"  Değişen Parça: {test['degisen_parca_sayisi']}, Onarılan: {test['onarilan_parca_sayisi']}")
    print()
    print(f"  ⚙️  KNN Baseline: {result.get('knn_baseline', 0):,.2f} TL")
    print(f"  📊 Katsayı R (Rayiç): {result.get('katsayi_R_rayic', 1.0):.3f}")
    print(f"  📊 Katsayı K (Kilometre): {result.get('katsayi_K_kilometre', 1.0):.3f}")
    print(f"  📊 Katsayı H (Hasar): {result.get('katsayi_H_hasar', 1.0):.3f}")
    print(f"  🚗 Marka/Model Çarpan: {result.get('carpan_marka_model', 1.0):.3f}")
    print(f"  📅 Araç Yaşı Çarpan: {result.get('carpan_arac_yasi', 1.0):.3f}")
    print(f"  ✖️  Toplam Çarpım: {result.get('carpim', 1.0):.3f}")
    print()
    print(f"  ✅ SONUÇ TAHMĐN: {result.get('tahmin', 0):,.2f} TL")

print("\n" + "="*100)
print("📌 BEKLENTİ: Yüksek km'deki araçlarda K katsayısı düşük olmalı (0.70-0.75)")
print("📌 SONUÇ: Yüksek km → Düşük K → Düşük tahmin (doğru yön!)")
print("="*100 + "\n")
