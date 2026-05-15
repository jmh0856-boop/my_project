from django.urls import path

from meals.views import MealDetailView, MealListCreateView, MealRecommendView

urlpatterns = [
    path("", MealListCreateView.as_view(), name="meal-list"),  # 목록 조회, 생성
    path(
        "<int:pk>/", MealDetailView.as_view(), name="meal-detail"
    ),  # 단건 조회, 수정, 삭제
    path("recommend/", MealRecommendView.as_view(), name="meal-recommend"),  # 추천 API
]
