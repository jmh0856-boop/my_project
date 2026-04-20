from django.conf import settings  # Django가 직접 제공하는 설정 접근 도구
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Meal(models.Model):
    CATEGORY_CHOICES = [
        ("한식", "한식"),
        ("중식", "중식"),
        ("양식", "양식"),
        ("분식", "분식"),
        ("일식", "일식"),
    ]

    menu_name = models.CharField(max_length=100)  # 메뉴명
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # 카테고리
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]  # 1~5 제한
    )
    eaten_at = models.DateField()  # 먹은 날짜
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # 유저 FK

    def __str__(self):
        return f"{self.owner} - {self.menu_name}"
