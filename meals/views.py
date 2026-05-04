from drf_spectacular.utils import OpenApiParameter, extend_schema  # Swagger 문서화 도구
from rest_framework import status  # HTTP 상태코드 모음
from rest_framework.permissions import IsAuthenticated  # 로그인 유저만 접근 가능
from rest_framework.response import Response  # JSON 응답 클래스
from rest_framework.views import APIView  # API 뷰 기본 클래스

from core.exceptions import NotFoundException  # 데이터 없음 예외
from meals.serializers import (  # 요청/응답 Serializer
    MealRequestSerializer,
    MealResponseSerializer,
)
from meals.services import MealService  # 식사기록 비즈니스 로직


class MealListCreateView(APIView):
    # 목록 조회(GET)와 생성(POST)을 담당하는 뷰
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="식사기록 목록 조회", responses=MealResponseSerializer)
    def get(self, request):
        # 서비스 호출 → 본인 식사기록 목록 조회
        meals = MealService.get_meals(user=request.user)
        serializer = MealResponseSerializer(meals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="식사기록 생성",
        request=MealRequestSerializer,
        responses=MealResponseSerializer,
    )
    def post(self, request):
        # 요청 데이터 검증
        serializer = MealRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        meal = MealService.create_meal(
            user=request.user,
            data=serializer.validated_data,
        )
        return Response(
            MealResponseSerializer(meal).data, status=status.HTTP_201_CREATED
        )


class MealDetailView(APIView):
    # 단건 조회(GET), 수정(PUT), 삭제(DELETE)를 담당하는 뷰
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="식사기록 단건 조회", responses=MealResponseSerializer)
    def get(self, request, pk):
        # 단건 조회
        meal = MealService.get_meal(pk=pk, user=request.user)
        serializer = MealResponseSerializer(meal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="식사기록 수정",
        request=MealRequestSerializer,
        responses=MealResponseSerializer,
    )
    def put(self, request, pk):
        # 수정
        meal = MealService.get_meal(pk=pk, user=request.user)
        serializer = MealRequestSerializer(meal, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_meal = MealService.update_meal(
            meal=meal,
            data=serializer.validated_data,
        )
        return Response(
            MealResponseSerializer(updated_meal).data, status=status.HTTP_200_OK
        )

    @extend_schema(summary="식사기록 삭제")
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
        summary="메뉴 추천",
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
        ],
    )
    def get(self, request):
        category = request.query_params.get("category")

        try:
            days = (
                int(request.query_params.get("days"))
                if request.query_params.get("days")
                else None
            )
            min_rating = (
                float(request.query_params.get("min_rating"))
                if request.query_params.get("min_rating")
                else None
            )
        except ValueError:
            return Response(
                {"error": "올바른 숫자를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
