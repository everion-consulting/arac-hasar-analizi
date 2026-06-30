from django.urls import path, re_path

from .views import csrf, frontend_login, logout, predict, predict_bearer, prediction_history, serve_frontend

urlpatterns = [
    # CSRF cookie üretmek için endpoint
    path("auth/csrf", csrf, name="csrf"),
    # Normal frontend kullanıcı girişi için endpoint
    path("auth/login", frontend_login, name="frontend_login"),
    # Logout endpoint'i
    path("auth/logout", logout, name="logout"),
    # Frontend /predict (slashesiz) çağırdığı için pattern'i slashesiz tanımlıyoruz.
    # Böylece APPEND_SLASH devreye girmez ve POST redirect olmadan direkt çalışır.
    path("predict", predict, name="predict"),
    path("predict/bearer", predict_bearer, name="predict_bearer"),
    # Geçmiş tahminler endpoint'i
    path("predictions/history", prediction_history, name="prediction_history"),
    # Frontend SPA - tüm diğer route'lar index.html'e yönlendirilir
    re_path(r'^(?!admin|api|auth|predict|static).*$', serve_frontend, name='frontend'),
]

