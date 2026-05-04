# 이메일 + 비밀번호가 맞는지 확인해주는 django 내장함수
from django.contrib.auth import authenticate

# JWT 토큰 발급해주는 클래스
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from core.exceptions import InvalidCredentialsException


class AuthService:

    @staticmethod
    def register(email, username, password):
        # 유저 생성 후 반환
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
        )
        return user

    @staticmethod
    def login(email, password):
        # 이메일 + 비밀번호 인증
        user = authenticate(email=email, password=password)

        if user is None:
            raise InvalidCredentialsException()

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "token_type": "bearer",
        }
