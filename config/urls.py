from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),  # 회원가입/로그인
    path("api/meals/", include("meals.urls")),  # 식사기록 CRUD
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # API 스키마(구조) 정보를 JSON으로 제공하는 URL
    # Swagger UI가 이 URL에서 API 정보를 읽어옴
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),
    # Swagger UI를 보여주는 URL
    # http://localhost:8000/api/docs/ 접속하면 API 문서 확인 가능
]
