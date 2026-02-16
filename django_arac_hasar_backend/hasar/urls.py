from django.urls import path

from .views import csrf, frontend_login, predict

urlpatterns = [
    # CSRF cookie üretmek için endpoint
    path("auth/csrf", csrf, name="csrf"),
    # Normal frontend kullanıcı girişi için endpoint
    path("auth/login", frontend_login, name="frontend_login"),
    # Frontend /predict (slashesiz) çağırdığı için pattern'i slashesiz tanımlıyoruz.
    # Böylece APPEND_SLASH devreye girmez ve POST redirect olmadan direkt çalışır.
    path("predict", predict, name="predict"),
]

