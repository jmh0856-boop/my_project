from drf_spectacular.utils import extend_schema
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
