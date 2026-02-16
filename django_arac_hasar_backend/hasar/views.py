import pandas as pd
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import FrontendUser, HasarTahmin
from .serializers import PredictRequestSerializer
from .services import get_knn_model


@api_view(["POST"])
@permission_classes([AllowAny])
def frontend_login(request):
    """
    Normal frontend kullanıcıları için login endpoint'i.
    - Django admin kullanıcılarından ayrı FrontendUser modelini kullanır.
    - Sadece aktif FrontendUser kayıtlarının girişine izin verir.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "Kullanıcı adı ve şifre zorunludur."},
            status=400,
        )

    # Önce Django'nun normal User modeline göre kimlik doğrulaması yap
    auth_user = authenticate(request, username=username, password=password)
    if auth_user is None or not auth_user.is_active:
        return Response(
            {"detail": "Geçersiz kullanıcı adı veya şifre."},
            status=400,
        )

    # Bu kullanıcı aynı zamanda FrontendUser tablosunda tanımlı mı (ayrı rol)?
    if not FrontendUser.objects.filter(username=auth_user.username, is_active=True).exists():
        return Response(
            {"detail": "Geçersiz kullanıcı adı veya şifre."},
            status=400,
        )

    # Django session oluştur
    django_login(request, auth_user)

    # Giriş başarılı, özet bilgi dön
    return Response(
        {
            "detail": "Giriş başarılı.",
            "username": auth_user.username,
        }
    )


@api_view(["POST"])
def predict(request):
    """
    /predict endpoint'i:
    - Request verisini validate eder
    - FastAPI'deki ile aynı preprocessing'i yapar
    - ML modelinden tahmin alır
    - Sonucu DB'ye kaydeder
    - Özet JSON response döner
    """
    serializer = PredictRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = dict(serializer.validated_data)

    # String alanları normalize et
    for key in ["degisen_aciklama", "onarilan_aciklama", "marka", "model"]:
        value = data.get(key)
        if isinstance(value, str):
            data[key] = value.strip().lower()

    # degisen_parcalar / onarilan_parcalar içinden parca_katsayilari üret
    def normalize_islem_turu(islem):
        if not isinstance(islem, str):
            return islem
        islem_lower = islem.lower()
        if "degisim" in islem_lower:
            return "degisim"
        if "onarim" in islem_lower:
            return "onarim"
        return islem_lower

    parca_katsayilari = []
    for p in data.get("degisen_parcalar", []) or []:
        parca_kodu = p.get("parca_kodu", "")
        islem_turu = normalize_islem_turu(p.get("islemTuru", "degisim"))
        seviye = p.get("seviye", "hafif") or "hafif"
        parca_katsayilari.append(
            {
                "parca_kodu": parca_kodu,
                "islem_turu": islem_turu,
                "hasar_seviyesi": seviye,
            }
        )

    for p in data.get("onarilan_parcalar", []) or []:
        parca_kodu = p.get("parca_kodu", "")
        islem_turu = normalize_islem_turu(p.get("islemTuru", "onarim"))
        seviye = p.get("seviye", "hafif") or "hafif"
        parca_katsayilari.append(
            {
                "parca_kodu": parca_kodu,
                "islem_turu": islem_turu,
                "hasar_seviyesi": seviye,
            }
        )

    data["parca_katsayilari"] = parca_katsayilari

    # DataFrame oluştur + tahmin yap
    df = pd.DataFrame([data])
    model = get_knn_model()

    try:
        result = model.predict(df)

        if isinstance(result, dict):
            tahmini = float(result.get("tahmin", 0))
            min_val = float(result.get("min", 0))
            max_val = float(result.get("max", 0))
            uyari = result.get("uyari")
            katsayi_H_hasar = result.get("katsayi_H_hasar")
            knn_baseline = result.get("knn_baseline")
        else:
            tahmini = float(result[0]) if hasattr(result, "__getitem__") else float(result)
            min_val = tahmini * 0.9
            max_val = tahmini * 1.1
            uyari = None
            katsayi_H_hasar = None
            knn_baseline = None

        # DB'ye kaydet
        hasar = HasarTahmin.objects.create(
            rayic_bedel=data["rayic_bedel"],
            hasar_bedeli=data["hasar_bedeli"],
            degisen_parca_sayisi=data["degisen_parca_sayisi"],
            onarilan_parca_sayisi=data["onarilan_parca_sayisi"],
            arac_kilometresi=data["arac_kilometresi"],
            arac_yasi=data.get("arac_yasi") or 0,
            marka=data.get("marka"),
            model=data.get("model"),
            arac_turu=data.get("arac_turu"),
            arac_kodu=data.get("arac_kodu"),
            degisen_parcalar=data.get("degisen_parcalar"),
            onarilan_parcalar=data.get("onarilan_parcalar"),
            parca_katsayilari=parca_katsayilari,
            tahmini=tahmini,
            min_deger=min_val,
            max_deger=max_val,
            uyari=uyari,
            katsayi_H_hasar=katsayi_H_hasar,
            knn_baseline=knn_baseline,
        )

        # Frontend'e dönecek özet JSON
        response_data = {
            "min": round(min_val, 2),
            "max": round(max_val, 2),
            "tahmini": round(tahmini, 2),
            "uyari": uyari,
            "rayic_bedel": float(data.get("rayic_bedel", 0)),
            "katsayi_H_hasar": katsayi_H_hasar,
            "knn_baseline": knn_baseline,
            "id": hasar.id,
        }
        return Response(response_data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    """
    CSRF cookie üretmek için basit endpoint.
    Frontend bu endpoint'e GET atarak csrftoken cookie'sini alır.
    """
    return Response({"csrfToken": get_token(request)})


@api_view(["POST"])
def logout(request):
    """
    Django session'ını sonlandırmak için güvenli logout endpoint'i.
    CSRF korumalıdır, bu yüzden frontend X-CSRFToken header'ı ile çağırmalıdır.
    """
    django_logout(request)
    return Response({"detail": "Çıkış yapıldı."})
