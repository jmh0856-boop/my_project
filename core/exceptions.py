from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidCredentialsException(APIException):
    # 로그인 실패 에러 (이메일 또는 비밀번호 불일치)
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "이메일 또는 비밀번호가 올바르지 않습니다."


class NotFoundException(APIException):
    # 데이터 없음 에러
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "존재하지 않는 데이터입니다."


class InvalidInputException(APIException):
    # 잘못된 입력값 에러
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "올바른 숫자를 입력해주세요."
