from django.contrib.auth.base_user import BaseUserManager  # 유저 매니저 기본 클래스
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.models import TimeStampedModel  # 공통 날짜 필드 (create_at, updated_at)


class UserManager(BaseUserManager):  # 유저 생성 로직을 담당하는 매니저 클래스
    def create_user(
        self, email, username, password=None, **extra_fields
    ):  # 일반 유저 생성 메서드
        if not email:
            raise ValueError("이메일은 필수입니다.")  # 이메일 없으면 에러 발생

        email = self.normalize_email(
            email
        )  # 이메일 소문자 정규화 (TEST@GMAIL.COM -> test@gmail.com)
        user = self.model(
            email=email, username=username, **extra_fields
        )  # User 모델 인스턴스 생성 (아직 DB 저장 안됨)
        user.set_password(password)  # 비밀번호 해시 처리
        user.save(using=self._db)  # 현재 사용 중인 DB에 저장
        return user  # 생성된 유저 변환

    def create_superuser(self, email, username, password=None, **extra_fields):
        # 슈퍼유저 생성 메서드 (python manage.py createsuperuser 실행 시 호출)
        extra_fields.setdefault("is_staff", True)  # 관리자 페이지 접근 가능하도록 설정
        extra_fields.setdefault("is_superuser", True)  # 모든 권한 부여
        return self.create_user(
            email, username, password, **extra_fields
        )  # create_user 호출해서 슈퍼유저 생성


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    # AbstractBaseUser -> 기본 인증 기능
    # PermissionsMixin -> 권한 관련 기능
    # TimeStampedModel -> created_at, updated_at 자동 추가

    email = models.EmailField(unique=True)  # 이메일 필드 (중복 불가, 로그인 식별자)
    username = models.CharField(max_length=50)  # 유저명 필드 (최대 50자)
    is_active = models.BooleanField(
        default=True
    )  # 계정 활성화 여부 (False면 로그인 불가)
    is_staff = models.BooleanField(default=False)  # 관리자 페이지 접근 여부
    objects = UserManager()  # 커스텀 매니저 연결 (User.objects.create_user() 사용 가능)
    USERNAME_FIELD = "email"  # 로그인 식별자로 이메일 사용
    REQUIRED_FIELDS = ["username"]  # createsuperuser 시 추가 필수 입력 필드

    def __str__(self):
        return self.email  # 출력 시 이메일로 표시
