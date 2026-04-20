from django.urls import path

from accounts.views import LoginView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),  # 회원가입
    path("login/", LoginView.as_view()),  # 로그인
]
