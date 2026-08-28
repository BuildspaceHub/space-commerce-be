from django.conf import settings
from django.http import HttpResponse


class AuthCookieService:
    """Handles authentication-related cookies."""

    @staticmethod
    def set_refresh_cookie(response: HttpResponse, refresh_token: str,) -> None:
        response.set_cookie(
            key=settings.AUTH_REFRESH_COOKIE_NAME,
            value=refresh_token,
            max_age=settings.AUTH_REFRESH_COOKIE_MAX_AGE,
            httponly=settings.AUTH_REFRESH_COOKIE_HTTPONLY,
            secure=settings.AUTH_REFRESH_COOKIE_SECURE,
            samesite=settings.AUTH_REFRESH_COOKIE_SAMESITE,
            path=settings.AUTH_REFRESH_COOKIE_PATH,
        )

    @staticmethod
    def delete_refresh_cookie(response: HttpResponse) -> None:
        response.delete_cookie(
            key=settings.AUTH_REFRESH_COOKIE_NAME,
            path=settings.AUTH_REFRESH_COOKIE_PATH,
        )