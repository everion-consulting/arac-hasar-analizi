from django.urls import path

from .views import predict

urlpatterns = [
    # Frontend /predict (slashesiz) çağırdığı için pattern'i slashesiz tanımlıyoruz.
    # Böylece APPEND_SLASH devreye girmez ve POST redirect olmadan direkt çalışır.
    path("predict", predict, name="predict"),
]

