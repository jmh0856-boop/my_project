# 이메일 + 비밀번호가 맞는지 확인해주는 django 내장함수
from django.contrib.auth import authenticate
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
# JWT 토큰 발급해주는 클래스
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
# 요청/응답 Serializer 가져오기
from accounts.serializers import (LoginRequestSerializer,
                                  RegisterRequestSerializer,
                                  TokenResponseSerializer,
                                  UserResponseSerializer)


class RegisterView(APIView):
    # 회원가입은 누구나 접근 가능 (로그인 안해도 됨)
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterRequestSerializer, responses=UserResponseSerializer)
    def post(self, request):
        # 클라이언트가 보낸 데이터 검증
        serializer = RegisterRequestSerializer(data=request.data)

        if serializer.is_valid():
            # 유저 생성
            user = User.objects.create_user(
                email=serializer.validated_data["email"],
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            # 응답 데이터 직렬화
            response_serializer = UserResponseSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        # 검증 실패 → 에러 메시지 반환 (400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # 로그인도 누구나 접근 가능
    permission_classes = [AllowAny]

    @extend_schema(request=LoginRequestSerializer, responses=TokenResponseSerializer)
    def post(self, request):
        # 요청 데이터 검증
        serializer = LoginRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            # DB에서 이메일 + 비밀번호 일치하는 유저 찾기
            user = authenticate(request, email=email, password=password)

            if user is None:
                # 401 = 인증 실패
                return Response(
                    {"message": "이메일 또는 비밀번호가 올바르지 않습니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # 유저 정보로 JWT 토큰 생성
            refresh = RefreshToken.for_user(user)

            # Access Token 문자열로 변환해서 반환
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "token_type": "bearer",
                }
            )

        # 검증 실패 → 에러 메시지 반환 (400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
