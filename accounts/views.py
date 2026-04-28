# Swagger 요청 스키마 정의 데코레이터
from drf_spectacular.utils import extend_schema

# HTTP 상태코드 모음 (200, 201, 400, 401 등)
from rest_framework import status

# 누구나 접근 가능 (로그인 없이도 됨)
from rest_framework.permissions import AllowAny

# API 응답을 JSON으로 만들어주는 클래스
from rest_framework.response import Response

# API 뷰의 기본 클래스 (DRF 제공)
from rest_framework.views import APIView

# 요청/응답 Serializer 가져오기
from accounts.serializers import (
    LoginRequestSerializer,
    RegisterRequestSerializer,
    TokenResponseSerializer,
    UserResponseSerializer,
)

# services.py 호출
from accounts.services import AuthService


class RegisterView(APIView):
    # 회원가입은 누구나 접근 가능 (로그인 안해도 됨)
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterRequestSerializer, responses=UserResponseSerializer)
    def post(self, request):
        # 클라이언트가 보낸 데이터 검증
        serializer = RegisterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.register(
            email=serializer.validated_data["email"],
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        response_serializer = UserResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    # 로그인도 누구나 접근 가능
    permission_classes = [AllowAny]

    @extend_schema(request=LoginRequestSerializer, responses=TokenResponseSerializer)
    def post(self, request):
        # 요청 데이터 검증
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AuthService.login(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        return Response(result, status=status.HTTP_200_OK)
