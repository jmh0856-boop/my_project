from django.contrib.auth import (
    authenticate,
)  # 이메일 + 비밀번호가 맞는지 확인해주는 django 내장함수
from rest_framework import status  # HTTP 상태코드 모음 (200, 201, 400, 401 등)
from rest_framework.response import Response  # API 응답을 JSON으로 만들어주는 클래스
from rest_framework.views import APIView  # API 뷰의 기본 블래스 (DRF 제공)
from rest_framework.permissions import AllowAny  # 누구나 접근 가능 (로그인 없이도 됨)
from rest_framework_simplejwt.tokens import RefreshToken  # JWT 토큰 발급해주는 클래스
from accounts.serializers import (
    RegisterSerializer,
    LoginSerializer,
)  # 우리가 만든 시리얼라이저 가져오기


class RegisterView(APIView):  # APIView 상속 -> POST, GET 등 HTTP 메서드 사용 가능
    permission_classes = [AllowAny]  # 회원가입은 누구나 접근 가능 (로그인 안해도 됨)

    def post(
        self, request
    ):  # POST 오면 실행되는 함수, request = 클라이언트가 보낸 데이터
        serializer = RegisterSerializer(
            data=request.data
        )  # 클라이언트가 보낸 JSON, RegisterSerializer 데이터 넣기

        if serializer.is_valid():  # 데이터 검증 (username, email, password 형식 맞는지)
            serializer.save()  # 검증 통과 -> DB에 저장 (creat() 실행됨)
            return Response(
                {"message": "회원가입이 완료되었습니다."},
                status=status.HTTP_201_CREATED,  # 201 = 생성 완료
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 검증 실패 -> 에러 메세지 변환
        # 400 = 잘못된 요청


class LoginView(APIView):
    permission_classes = [AllowAny]  # 로그인도 누구나 접근 가능

    def post(self, request):
        serializer = LoginSerializer(data=request.data)  # 이메일 + 비밀번호 데이터 받기

        if serializer.is_valid():  # 이메일 형식, 비밀번호 있는지 검증
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            # validated_data = 검증 완료된 데이터에서 꺼내기

            user = authenticate(request, email=email, password=password)
            # DB에서 이메일 + 비밀번호 일치하는 유저 찾기
            # 없으면 None 반환

            if user is None:
                return Response(
                    {"message": "이메일 또는 비밀번호가 올바르지 않습니다."},
                    status=status.HTTP_401_UNAUTHORIZED,  # 401 = 인증 실패
                )

            refresh = RefreshToken.for_user(user)
            # 유저 정보로 JWT 토큰 생성
            # refresh = Refresh Token
            # refresh.access_token = Access Token

            return Response(
                {
                    "access_token": str(
                        refresh.access_token
                    ),  # Access Token 문자열로 변환해서 반환
                    "token_type": "bearer",
                    # 토큰 타입 (항상 bearer)
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 검증 실패 -> 에러 메세지 변환
        # 400 = 잘못된 요청
