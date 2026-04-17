# 파이썬 3.11 기반 경량 이미지 사용
FROM python:3.11-slim

# 컨테이너 안에서 작업 디렉토리를 /app으로 설정
WORKDIR /app

# requirements.txt를 컨테이너 /app에 복사
COPY requirements.txt .
# 패키지 설치
RUN pip install -r requirements.txt

# 현재 로컬 코드 전체를 컨테이너 /app에 복사
COPY . .

# 컨테이너 실행 시 Django 서버 시작
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
