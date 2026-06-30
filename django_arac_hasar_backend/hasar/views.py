import os
from pathlib import Path

from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .authentication import BearerTokenAuthentication
from .models import FrontendUser, HasarTahmin
from .serializers import PredictRequestSerializer
from .services import execute_prediction


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

    # Giriş başarılı, özet bilgi + user_id dön
    return Response(
        {
            "detail": "Giriş başarılı.",
            "username": auth_user.username,
            "user_id": auth_user.id,
        }
    )


@api_view(["POST"])
def predict(request):
    """
    /predict endpoint'i (session auth):
    - Request verisini validate eder
    - ML modelinden tahmin alır
    - Sonucu DB'ye kaydeder
    """
    serializer = PredictRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        frontend_user = None
        if request.user.is_authenticated:
            frontend_user = FrontendUser.objects.filter(
                username=request.user.username, is_active=True
            ).first()
        response_data = execute_prediction(
            serializer.validated_data,
            user=request.user if request.user.is_authenticated else None,
            frontend_user=frontend_user,
            save_to_db=True,
        )
        return Response(response_data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([AllowAny])
def predict_bearer(request):
    """
    /api/predict/bearer — dış entegrasyonlar için.
    Bearer token ile çalışır, DB'ye yazmaz; response formatı /predict ile aynı (id hariç).
    """
    serializer = PredictRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        response_data = execute_prediction(
            serializer.validated_data,
            save_to_db=False,
        )
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


@api_view(["GET", "POST"])
def prediction_history(request):
    """
    Kullanıcının geçmiş tahminlerini getirir.
    Sadece giriş yapmış kullanıcılar için çalışır.
    """
    if not request.user.is_authenticated:
        return Response({"detail": "Giriş yapmanız gerekiyor."}, status=401)

    # İsteğe bağlı user_id:
    # - GET ise query paramdan
    # - POST ise JSON body'den okunur
    if request.method == "POST":
        requested_user_id = request.data.get("user_id")
    else:
        requested_user_id = request.query_params.get("user_id")
    if requested_user_id is not None:
        try:
            requested_user_id = int(requested_user_id)
        except (TypeError, ValueError):
            return Response({"detail": "Geçersiz user_id."}, status=400)

        if requested_user_id != request.user.id:
            return Response({"detail": "Bu kullanıcı için yetkiniz yok."}, status=403)
        user_id = requested_user_id
    else:
        user_id = request.user.id

    # Sadece HasarTahmin.user FK'sine göre filtrele
    tahminler = HasarTahmin.objects.filter(user_id=user_id).order_by("-created_at")
    
    # Serialize et
    history_data = []
    for tahmin in tahminler:
        history_data.append({
            "id": tahmin.id,
            "marka": tahmin.marka,
            "model": tahmin.model,
            "arac_turu": tahmin.arac_turu,
            "arac_kodu": tahmin.arac_kodu,
            "arac_yasi": tahmin.arac_yasi,
            "arac_kilometresi": tahmin.arac_kilometresi,
            "tahmini": float(tahmin.tahmini) if tahmin.tahmini is not None else None,
            "min_deger": float(tahmin.min_deger) if tahmin.min_deger is not None else None,
            "max_deger": float(tahmin.max_deger) if tahmin.max_deger is not None else None,
            "rayic_bedel": float(tahmin.rayic_bedel),
            "hasar_bedeli": float(tahmin.hasar_bedeli),
            "degisen_parcalar": tahmin.degisen_parcalar or [],
            "onarilan_parcalar": tahmin.onarilan_parcalar or [],
            "created_at": tahmin.created_at.isoformat() if tahmin.created_at else None,
        })
    
    return Response(
        {
            "results": history_data,
            "count": len(history_data),
            "user_id": user_id,
        }
    )


def serve_frontend(request):
    """
    Frontend SPA'yı serve eder. Tüm route'lar index.html'e yönlendirilir.
    Frontend build edilmişse dist/index.html'i, yoksa root'taki index.html'i kullanır.
    """
    # Frontend build klasörü (dist) varsa onu kullan, yoksa root'taki index.html'i kullan
    build_path = Path(settings.BASE_DIR.parent) / "dist" / "index.html"
    root_path = Path(settings.BASE_DIR.parent) / "index.html"
    
    if build_path.exists():
        index_file = build_path
    elif root_path.exists():
        index_file = root_path
    else:
        # Fallback: basit HTML döndür
        return HttpResponse(
            """
            <!DOCTYPE html>
            <html>
            <head><title>Frontend Build Edilmeli</title></head>
            <body>
                <h1>Frontend build edilmeli</h1>
                <p>Lütfen <code>npm run build</code> komutunu çalıştırın.</p>
            </body>
            </html>
            """,
            content_type="text/html"
        )
    
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type="text/html")
    except Exception as e:
        return HttpResponse(f"Error loading frontend: {str(e)}", status=500)
