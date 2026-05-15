from rest_framework import serializers

from meals.models import Meal


# 식사기록 요청 Serializer (입력 데이터 검증)
class MealRequestSerializer(serializers.Serializer):
    menu_name = serializers.CharField(max_length=100)
    category = serializers.ChoiceField(choices=Meal.CATEGORY_CHOICES)
    rating = serializers.DecimalField(
        max_digits=2, decimal_places=1, min_value=1, max_value=5
    )
    eaten_at = serializers.DateField()


# 식사기록 응답 Serializer (출력 데이터 형식)
class MealResponseSerializer(serializers.ModelSerializer):
    class Meta:  # 이 Serializer의 설정 정보 (Django 약속)
        model = Meal  # 어떤 모델과 연결할지 -> Meal 모델
        fields = [
            "id",
            "menu_name",
            "category",
            "rating",
            "eaten_at",
            "owner",
        ]  # 응답/요청에서 사용할 필드 목록
        read_only_fields = ["owner"]  # views.py에서 request.user로 자동 저장
