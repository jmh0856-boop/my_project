from rest_framework import serializers

from accounts.models import User


# 회원가입 요청 (입력 데이터 검증)
class RegisterRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    # write_only=True -> 응답에 비밀번호 포함 안함

    def validate_email(self, value):
        # 이메일 중복 검증
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value


# 로그인 요청 (입력 데이터 검증)
class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    # write_only=True -> 응답에 비밀번호 포함 안함


# 유저 정보 응답 (출력 데이터 형식)
class UserResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "created_at")
        # 응답에 포함할 필드만 선택


# 토큰 응답 (출력 데이터 형식)
class TokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField()
