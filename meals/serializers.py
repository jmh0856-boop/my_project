from rest_framework import serializers

from meals.models import Meal


class MealSerializer(serializers.ModelSerializer):
    # Meal 모델과 연결된 번역기 클래스
    # ModelSerializer 상속 → JSON ↔ Python 변환 기능 포함

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
