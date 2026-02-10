"""Backend API test - Parça katsayısı testi"""
import requests
import json

# API endpoint
url = "http://localhost:8000/predict"

# Test 1: Motor Kaputu (A.10 - Onarım Orta: 0.75)
test1 = {
    "rayic_bedel": 500000,
    "hasar_bedeli": 50000,
    "degisen_parca_sayisi": 0,
    "onarilan_parca_sayisi": 1,
    "arac_kilometresi": 50000,
    "marka": "Mercedes",
    "model": "C180",
    "degisen_parcalar": [],
    "onarilan_parcalar": [
        {
            "parca_kodu": "A.10",  # MOTOR KAPUTU
            "islemTuru": "onarim",
            "seviye": "orta"
        }
    ]
}

# Test 2: Sağ Arka Çamurluk (A.23 - Onarım Orta: 1.00)
test2 = {
    "rayic_bedel": 500000,
    "hasar_bedeli": 50000,
    "degisen_parca_sayisi": 0,
    "onarilan_parca_sayisi": 1,
    "arac_kilometresi": 50000,
    "marka": "Mercedes",
    "model": "C180",
    "degisen_parcalar": [],
    "onarilan_parcalar": [
        {
            "parca_kodu": "A.23",  # SAĞ ARKA ÇAMURLUK
            "islemTuru": "onarim",
            "seviye": "orta"
        }
    ]
}

print("\n" + "="*80)
print("BACKEND API TEST - PARÇA KATSAYISI")
print("="*80)

print("\n📋 Test 1: Motor Kaputu (Katsayı: 0.75)")
response1 = requests.post(url, json=test1)
result1 = response1.json()
print(f"   Sonuç: {result1.get('tahmini', 0):,.2f} TL")
print(f"   KNN Baseline: {result1.get('knn_baseline', 0):,.2f} TL")
print(f"   Katsayı H: {result1.get('katsayi_H_hasar', 1.0):.4f}")

print("\n📋 Test 2: Çamurluk (Katsayı: 1.00)")
response2 = requests.post(url, json=test2)
result2 = response2.json()
print(f"   Sonuç: {result2.get('tahmini', 0):,.2f} TL")
print(f"   KNN Baseline: {result2.get('knn_baseline', 0):,.2f} TL")
print(f"   Katsayı H: {result2.get('katsayi_H_hasar', 1.0):.4f}")

print("\n" + "="*80)
if result1.get('tahmini', 0) != result2.get('tahmini', 0):
    print("✅ BAŞARILI: Farklı parçalar farklı sonuçlar veriyor!")
    print(f"   Fark: {abs(result1.get('tahmini', 0) - result2.get('tahmini', 0)):,.2f} TL")
else:
    print("❌ BAŞARISIZ: İki parça aynı sonucu veriyor!")
print("="*80 + "\n")
