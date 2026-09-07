from django.urls import path

from .views import TokenRefreshView, TestProtectedView


urlpatterns = [
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("test/protected/", TestProtectedView.as_view(), name="test-protected"),
]