from django.db import models


class HasarTahmin(models.Model):
    # Kullanıcının girdiği temel sayısal alanlar
    rayic_bedel = models.FloatField()
    hasar_bedeli = models.FloatField()
    degisen_parca_sayisi = models.IntegerField()
    onarilan_parca_sayisi = models.IntegerField()
    arac_kilometresi = models.FloatField()
    arac_yasi = models.IntegerField()

    # Araç bilgileri
    marka = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    arac_turu = models.CharField(max_length=100, blank=True, null=True)
    arac_kodu = models.CharField(max_length=50, blank=True, null=True)

    # Liste / JSON alanları (frontend + backend tarafında oluşturulanlar)
    degisen_parcalar = models.JSONField(blank=True, null=True)
    onarilan_parcalar = models.JSONField(blank=True, null=True)
    parca_katsayilari = models.JSONField(blank=True, null=True)

    # Tahmin sonuçları
    tahmini = models.FloatField(blank=True, null=True)
    min_deger = models.FloatField(blank=True, null=True)
    max_deger = models.FloatField(blank=True, null=True)
    uyari = models.TextField(blank=True, null=True)
    katsayi_H_hasar = models.FloatField(blank=True, null=True)
    knn_baseline = models.FloatField(blank=True, null=True)

    # Meta bilgiler
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.marka} {self.model} - {self.tahmini or '-'}"