from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import LoginView, RegisterView

TokenRefreshView = extend_schema(summary="토큰 갱신")(TokenRefreshView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # 회원가입
    path("login/", LoginView.as_view(), name="login"),  # 로그인
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token-refresh"
    ),  # 토큰 갱신
]
