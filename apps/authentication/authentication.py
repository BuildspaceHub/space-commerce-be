from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Authentication backend for SpaceCommerce.

    Access tokens are supplied using:

        Authorization: Bearer <access_token>

    Refresh tokens are handled separately by the refresh
    endpoint and are stored in an HttpOnly cookie.
    """

    pass