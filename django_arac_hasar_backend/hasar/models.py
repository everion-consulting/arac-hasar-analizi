from django.db import models
from django.contrib.auth.models import User


class FrontendUser(models.Model):
    """
    Admin panel kullanıcılarından tamamen ayrı, sadece normal frontend girişleri
    için kullanılacak kullanıcı modeli.
    Şifreler Django'nun hash mekanizması ile saklanır.
    """

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password: str) -> None:
        from django.contrib.auth.hashers import make_password

        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        from django.contrib.auth.hashers import check_password

        return check_password(raw_password, self.password)

    def __str__(self) -> str:
        return self.username


class HasarTahmin(models.Model):
    # Kullanıcı bilgisi (opsiyonel - mevcut kayıtlar için null olabilir)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='hasar_tahminleri')

    # Frontend kullanıcı bilgisi (asıl eşleştirme bununla yapılacak)
    frontend_user = models.ForeignKey(
        FrontendUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tahminler",
    )
    
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