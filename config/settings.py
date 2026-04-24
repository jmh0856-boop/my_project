import os
from pathlib import Path

from dotenv import load_dotenv

# .env 파일 읽기
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS: list = ["localhost", "0.0.0.0", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 서드파티
    "rest_framework",
    # 로컬 앱
    "accounts",
    "meals",
    "drf_spectacular",  # Swagger 추가
]

# 커스텀 User 모델 지정
AUTH_USER_MODEL = "accounts.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # PostgreSQL 사용
        "NAME": os.getenv("POSTGRES_DB"),  # .env에서 DB 이름 읽기
        "USER": os.getenv("POSTGRES_USER"),  # .env에서 유저 읽기
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),  # .env에서 비밀번호 읽기
        "HOST": os.getenv("DB_HOST"),  # .env에서 호스트 읽기
        "PORT": os.getenv("DB_PORT"),  # .env에서 포트 읽기
    }
}

# JWT 인증 설정
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.authentication.CustomJWTAuthentication",  # 커스텀 JWT 인증
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # 기본 로그인 필요
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # 추가
}

# Swagger 설정
SPECTACULAR_SETTINGS = {
    "TITLE": "혼밥 메뉴 추천 API",
    "DESCRIPTION": "혼밥 메뉴 추천 서비스 API 문서",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": "/api/",
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
    "SECURITY": [{"BearerAuth": []}],
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),  # 액세스 토큰 1시간
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # 리프레시 토큰 7일
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ko-kr"  # 한국어

TIME_ZONE = "Asia/Seoul"  # 한국 시간

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
