from rest_framework import serializers

from .models import HasarTahmin


class PredictRequestSerializer(serializers.Serializer):
    # Kullanıcıdan gelen tahmin isteği payload'ı
    rayic_bedel = serializers.FloatField()
    hasar_bedeli = serializers.FloatField()
    degisen_parca_sayisi = serializers.IntegerField()
    onarilan_parca_sayisi = serializers.IntegerField()
    arac_kilometresi = serializers.FloatField()
    arac_yasi = serializers.IntegerField(required=False, allow_null=True)

    marka = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    model = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    arac_turu = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    arac_kodu = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    degisen_aciklama = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    onarilan_aciklama = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    degisen_parcalar = serializers.ListField(
        child=serializers.DictField(), required=False, allow_empty=True
    )
    onarilan_parcalar = serializers.ListField(
        child=serializers.DictField(), required=False, allow_empty=True
    )

    def validate(self, attrs):
        # Buraya istersen ek iş kuralları ekleyebilirsin
        return attrs


class HasarTahminSerializer(serializers.ModelSerializer):
    class Meta:
        model = HasarTahmin
        fields = "__all__"

