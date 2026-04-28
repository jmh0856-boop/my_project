from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import NotFoundException
from meals.serializers import MealRequestSerializer, MealResponseSerializer
from meals.services import MealService


class MealListCreateView(APIView):
    # 목록 조회(GET)와 생성(POST)을 담당하는 뷰
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 서비스 호출 → 본인 식사기록 목록 조회
        meals = MealService.get_meals(user=request.user)
        serializer = MealResponseSerializer(meals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=MealRequestSerializer, responses=MealResponseSerializer)
    def post(self, request):
        # 요청 데이터 검증
        serializer = MealRequestSerializer(data=request.data)
        if serializer.is_valid():
            # 서비스 호출 → 식사기록 생성
            meal = MealService.create_meal(
                user=request.user,
                data=serializer.validated_data,
            )
            return Response(
                MealResponseSerializer(meal).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealDetailView(APIView):
    # 단건 조회(GET), 수정(PUT), 삭제(DELETE)를 담당하는 뷰
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # 단건 조회
        meal = MealService.get_meal(pk=pk, user=request.user)
        serializer = MealResponseSerializer(meal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=MealRequestSerializer, responses=MealResponseSerializer)
    def put(self, request, pk):
        # 수정
        meal = MealService.get_meal(pk=pk, user=request.user)
        serializer = MealRequestSerializer(meal, data=request.data)
        if serializer.is_valid():
            # 서비스 호출 → 수정
            updated_meal = MealService.update_meal(
                meal=meal,
                data=serializer.validated_data,
            )
            return Response(
                MealResponseSerializer(updated_meal).data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # 삭제
        meal = MealService.get_meal(pk=pk, user=request.user)
        # 서비스 호출 → 삭제
        MealService.delete_meal(meal=meal)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class MealRecommendView(APIView):
    # 로그인한 유저만 접근 가능
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category", description="카테고리 선택", required=False, type=str
            ),
            OpenApiParameter(
                name="days",
                description="최근 N일 이내 먹은 메뉴 제외",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="min_rating", description="최소 평점", required=False, type=int
            ),
        ]
    )
    def get(self, request):
        category = request.query_params.get("category")
        days = request.query_params.get("days")
        min_rating = request.query_params.get("min_rating")

        # 서비스 호출 → 추천
        meal, reasons = MealService.recommend_meal(
            user=request.user,
            category=category,
            days=days,
            min_rating=min_rating,
        )

        if meal is None:
            raise NotFoundException()

        return Response(
            {
                "recommended_menu": meal.menu_name,
                "category": meal.category,
                "rating": meal.rating,
                "last_eaten": meal.eaten_at,
                "reasons": reasons,
            },
            status=status.HTTP_200_OK,
        )
