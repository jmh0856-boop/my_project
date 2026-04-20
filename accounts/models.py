from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # 이메일 중복 불가
    email = models.EmailField(unique=True)

    # 생성 일자 자동 저장
    created_at = models.DateTimeField(auto_now_add=True)

    # 이메일로 로그인하도록 설정
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
