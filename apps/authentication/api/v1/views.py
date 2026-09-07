from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from common.responses import success_response
from rest_framework.permissions import IsAuthenticated



class TokenRefreshView(APIView):
    """
    Refresh an access token using the refresh token
    stored in the HttpOnly authentication cookie.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get(
            settings.AUTH_REFRESH_COOKIE_NAME
        )

        if not refresh_token:
            return Response(
                {
                    "statusCode": status.HTTP_401_UNAUTHORIZED,
                    "message": "Refresh token is missing.",
                    "error": "AuthenticationError",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # JWT refresh implementation will go here.

        return Response(
            {
                "statusCode": status.HTTP_501_NOT_IMPLEMENTED,
                "message": "Token refresh is not implemented yet.",
                "error": "NotImplemented",
            },
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )



class TestProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "user_id": request.user.id,
                "email": request.user.email,
            }
        )