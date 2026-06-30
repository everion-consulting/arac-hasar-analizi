import os

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class BearerTokenAuthentication(BaseAuthentication):
    """
    Authorization: Bearer <token>
    Token sunucuda PREDICT_API_BEARER_TOKEN ortam değişkeni ile tanımlanır.
    """

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Bearer token gerekli.")

        token = auth_header[7:].strip()
        expected = os.getenv("PREDICT_API_BEARER_TOKEN", "")
        if not expected:
            raise AuthenticationFailed("API token yapılandırılmamış.")
        if token != expected:
            raise AuthenticationFailed("Geçersiz bearer token.")

        return (None, token)
