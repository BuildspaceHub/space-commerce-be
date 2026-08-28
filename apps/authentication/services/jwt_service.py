from typing import Any

from rest_framework_simplejwt.tokens import RefreshToken


class JWTService:
    """Service responsible for JWT operations."""

    @staticmethod
    def create_tokens_for_user(user) -> dict[str, str]:
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @staticmethod
    def refresh_tokens(refresh_tokens: str) :
        pass

    @staticmethod
    def blacklist_refresh_token(refresh_token: str) -> None:
        token = RefreshToken(refresh_token)
        token.blacklist()