import random
from datetime import date, timedelta

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status  # HTTP 상태코드 모음 (200, 201, 400, 403, 404 등)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response  # API 응답을 JSON으로 만들어주는 클래스
from rest_framework.views import APIView  # API 뷰의 기본 클래스

from core.permissions import IsOwner  # 우리가 만든 본인 확인 권한 클래스
from meals.models import Meal  # Meal 모델 가져오기
from meals.serializers import MealSerializer  # 우리가 만든 Meal 번역기 가져오기


class MealListCreateView(APIView):  # 목록 조회(GET)와 생성(POST)을 담당하는 뷰
    permission_classes = [IsAuthenticated]  # 로그인한 유저만 접근 가능

    def get(self, request):  # GET 요청 → 식사기록 목록 조회
        meals = Meal.objects.filter(
            owner=request.user
        )  # DB에서 로그인한 유저의 식사기록만 가져오기
        serializer = MealSerializer(
            meals, many=True
        )  # many=True → 여러 개의 데이터를 JSON으로 변환
        return Response(serializer.data)  # JSON으로 변환된 데이터 응답

    @extend_schema(request=MealSerializer)
    def post(self, request):  # POST 요청 -> 식사기록 생성
        serializer = MealSerializer(
            data=request.data
        )  # 클라이언트가 보낸 데이터를 Serializer에 넣기

        if serializer.is_valid():  # 데이터 검증
            serializer.save(owner=request.user)  # owner를 로그인한 유저로 자동 저장
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )  # 생성된 데이터 응답 (201)

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # 검증 실패 → 에러 응답 (400)


class MealDetailView(APIView):  # 단건 조회(GET), 수정(PUT), 삭제(DELETE)를 담당하는 뷰
    permission_classes = [IsAuthenticated]  # 로그인한 유저만 접근 가능

    def get_object(self, pk, user):
        # pk로 식사기록 찾고 권한 확인하는 공통 함수
        # 여러 메서드에서 반복되는 코드를 하나로 묶음

        try:
            meal = Meal.objects.get(pk=pk)  # pk로 식사기록 찾기

        except Meal.DoesNotExist:
            return None, Response(
                {"message": "존재하지 않는 식사기록입니다."},
                status=status.HTTP_404_NOT_FOUND,  # 없으면 404 반환
            )

        if meal.owner != user:
            return None, Response(
                {"message": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,  # 본인 것이 아니면 403 반환
            )
        return meal, None  # 정상이면 meal 반환, 에러는 None

    def get(self, request, pk):  # GET 요청 → 단건 조회
        meal, error = self.get_object(pk, request.user)
        # get_object로 meal 가져오기
        # error가 있으면 → 404 or 403

        if error:
            return error  # 에러 있으면 바로 반환

        serializer = MealSerializer(meal)  # meal을 JSON으로 변환
        return Response(serializer.data)  # 응답

    @extend_schema(request=MealSerializer)
    def put(self, request, pk):  # PUT 요청 → 수정
        meal, error = self.get_object(pk, request.user)
        if error:
            return error

        serializer = MealSerializer(
            meal, data=request.data
        )  # 기존 meal에 새 데이터 덮어쓰기

        if serializer.is_valid():
            serializer.save()  # 수정된 데이터 저장
            return Response(serializer.data)  # 수정된 데이터 응답 (200)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):  # DELETE 요청 → 삭제
        meal, error = self.get_object(pk, request.user)
        if error:
            return error

        meal.delete()  # DB에서 삭제

        return Response(
            {"message": "삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT,  # 204 = 삭제 완료 (응답 본문 없음)
        )


class MealRecommendView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인한 유저만 접근 가능

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
        category = request.query_params.get("category")  # 카테고리 파라미터
        days = request.query_params.get("days")  # 최근 N일 제외 파라미터
        min_rating = request.query_params.get("min_rating")  # 최소 평점 파라미터

        meals = Meal.objects.filter(owner=request.user)  # 본인 식사기록만 조회

        if category:
            meals = meals.filter(category=category)  # 카테고리 필터

        if days:
            exclude_date = date.today() - timedelta(days=int(days))  # N일 전 날짜 계산
            meals = meals.exclude(eaten_at__gte=exclude_date)  # N일 이내 먹은 메뉴 제외

        if min_rating:
            meals = meals.filter(rating__gte=min_rating)  # 최소 평점 필터

        if not meals.exists():
            return Response(
                {"message": "조건에 맞는 식사기록이 없습니다."},
                status=status.HTTP_404_NOT_FOUND,  # 404 = 데이터 없음
            )

        meals = meals.order_by("-rating")  # 평점 높은 순 정렬
        meal = random.choice(list(meals[:5]))  # 상위 5개 중 랜덤 추천

        reasons = []  # 추천 이유 리스트
        if days:
            reasons.append(f"최근 {days}일 이내 먹지 않았고")  # 날짜 조건 이유
        if min_rating:
            reasons.append(f"평점 {min_rating}점 이상이며")  # 평점 조건 이유
        reasons.append("평점이 높습니다.")  # 기본 이유

        return Response(
            {
                "recommended_menu": meal.menu_name,  # 추천 메뉴명
                "category": meal.category,  # 카테고리
                "rating": meal.rating,  # 평점
                "last_eaten": meal.eaten_at,  # 마지막으로 먹은 날짜
                "reasons": " ".join(reasons),  # 추천 이유 문자열로 합치기
            }
        )
