from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


@pytest.mark.django_db
def test_valid_access_token_authenticates_user(client, user):
    access_token = AccessToken.for_user(user)

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    response = client.get(
        "/api/v1/test/protected/"
    )

    assert response.status_code == 200
    assert response.data["user_id"] == user.id
    assert response.data["email"] == user.email


    @pytest.mark.django_db
    def test_missing_access_token_returns_401(client):
        response = client.get(
            "/api/v1/test/protected/"
        )

        assert response.status_code == 401


    @pytest.mark.django_db
    def test_invalid_authentication_header_returns_401(
        client,
    ):
        client.credentials(
            HTTP_AUTHORIZATION="InvalidToken abc123"
        )

        response = client.get(
            "/api/v1/test/protected/"
        )

        assert response.status_code == 401


    @pytest.mark.django_db
    def test_invalid_access_token_returns_401(client):
        client.credentials(
            HTTP_AUTHORIZATION="Bearer this-is-not-a-valid-jwt"
        )

        response = client.get(
            "/api/v1/test/protected/"
        )

        assert response.status_code == 401


    @pytest.mark.django_db
    def test_expired_access_token_returns_401(
        client,
        user,
    ):
        access_token = AccessToken.for_user(user)

        access_token["exp"] = int(
            (
                timezone.now()
                - timedelta(minutes=1)
            ).timestamp()
        )

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = client.get(
            "/api/v1/test/protected/"
        )

        assert response.status_code == 401


    @pytest.mark.django_db
    def test_refresh_token_cannot_authenticate_request(
        client,
        user,
    ):
        refresh_token = RefreshToken.for_user(user)

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh_token}"
        )

        response = client.get(
            "/api/v1/test/protected/"
        )

        assert response.status_code == 401


    @pytest.mark.django_db
    def test_token_for_nonexistent_user_returns_401(
        client,
        user,
    ):
        access_token = AccessToken.for_user(user)

        user.delete()

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = client.get(
            "/api/v1/test/protected/"
        )

        assert response.status_code == 401


    @pytest.mark.django_db
    def test_inactive_user_cannot_authenticate(
        client,
        user,
    ):
        user.is_active = False
        user.save(update_fields=["is_active"])

        access_token = AccessToken.for_user(user)

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = client.get(
            "/api/v1/test/protected/"
        )

        assert response.status_code == 401