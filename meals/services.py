import random
from datetime import date, timedelta

from core.exceptions import NotFoundException, PermissionDeniedException
from meals.models import Meal


class MealService:

    @staticmethod
    def get_meals(user):
        # 본인 식사기록 목록 조회
        return Meal.objects.filter(owner=user)

    @staticmethod
    def create_meal(user, data):
        # 식사기록 생성
        return Meal.objects.create(owner=user, **data)

    @staticmethod
    def get_meal(pk, user):
        try:
            meal = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            raise NotFoundException()

        if meal.owner != user:
            raise PermissionDeniedException()

        return meal

    @staticmethod
    def update_meal(meal, data):
        # 식사기록 수정
        for key, value in data.items():
            setattr(meal, key, value)
        meal.save(update_fields=list(data.keys()))
        return meal

    @staticmethod
    def delete_meal(meal):
        # 식사기록 삭제
        meal.delete()

    @staticmethod
    def recommend_meal(user, category=None, days=None, min_rating=None):
        # 본인 식사기록만 조회
        meals = Meal.objects.filter(owner=user)

        # 카테고리 필터
        if category:
            meals = meals.filter(category=category)

        # 최근 N일 이내 먹은 메뉴 제외
        if days:
            exclude_date = date.today() - timedelta(days=int(days))
            meals = meals.exclude(eaten_at__gte=exclude_date)

        # 최소 평점 필터
        if min_rating:
            meals = meals.filter(rating__gte=min_rating)

        if not meals.exists():
            return None, None

        # 평점 높은 순 정렬 후 상위 5개 중 랜덤 추천
        meals = meals.order_by("-rating")
        meal = random.choice(list(meals[:5]))

        # 추천 이유 생성
        reasons = []
        if days:
            reasons.append(f"최근 {days}일 이내 먹지 않았고")
        if min_rating:
            reasons.append(f"평점 {min_rating}점 이상이며")
        reasons.append("평점이 높습니다.")

        return meal, " ".join(reasons)
