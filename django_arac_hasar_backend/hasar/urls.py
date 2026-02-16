from django.urls import path

from .views import frontend_login, predict

urlpatterns = [
    # Frontend /predict (slashesiz) çağırdığı için pattern'i slashesiz tanımlıyoruz.
    # Böylece APPEND_SLASH devreye girmez ve POST redirect olmadan direkt çalışır.
    path("predict", predict, name="predict"),
    # Normal frontend kullanıcı girişi için endpoint
    path("auth/login", frontend_login, name="frontend_login"),
]

