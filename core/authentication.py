from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    # 기본 JWT 인증을 상속받아 커스텀 로직 추가 가능
    pass
