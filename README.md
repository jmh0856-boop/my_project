# 🍱 혼밥 메뉴 추천 서비스

혼자 밥을 먹을 때 메뉴를 고르기 어려운 사람들을 위한 **식사기록 기반 메뉴 추천 API 서비스**입니다.

---

## 🛠 기술 스택

| 분류 | 기술 |
|---|---|
| Backend | Python, Django, Django REST Framework |
| 인증 | JWT (djangorestframework-simplejwt) |
| Database | PostgreSQL |
| 인프라 | Docker, Docker Compose |
| API 문서 | Swagger (drf-spectacular) |
| 코드 품질 | pre-commit, black, isort, mypy |

---

## 📁 프로젝트 구조

```
my_project/
├── config/         # 프로젝트 설정
├── core/           # 공통 모델, 인증, 권한, 예외
├── accounts/       # 회원가입, 로그인
├── meals/          # 식사기록 CRUD, 메뉴 추천
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## ⚙️ 설치 및 실행

### 1. 환경변수 설정
```bash
# .env 파일 생성
SECRET_KEY=your_secret_key
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
```

### 2. Docker로 실행
```bash
docker-compose up --build
```

### 3. 마이그레이션
```bash
docker-compose exec web python manage.py migrate
```

### 4. API 문서 확인
```
http://localhost:8000/api/docs/
```

---

## 📌 주요 기능

### 1. 회원가입 / 로그인
- 이메일 + 비밀번호로 회원가입
- 이메일 중복 검증
- 비밀번호 해시 처리
- JWT 토큰 발급 (Access Token, Refresh Token)

### 2. 식사기록 CRUD
- 식사기록 생성, 조회, 수정, 삭제
- 본인 데이터만 접근 가능
- 카테고리: 한식, 중식, 양식, 분식, 일식
- 평점: 1.0 ~ 5.0 (소수점 지원)

### 3. 메뉴 추천
- 평점 높은 메뉴 우선 추천
- 카테고리별 필터링
- 최근 N일 이내 먹은 메뉴 제외
- 최소 평점 필터링
- 추천 이유 제공

---

## 🔑 API 엔드포인트

| Method | URL | 설명 | 인증 |
|---|---|---|---|
| POST | `/api/auth/register/` | 회원가입 | 불필요 |
| POST | `/api/auth/login/` | 로그인 | 불필요 |
| GET | `/api/meals/` | 식사기록 목록 조회 | 필요 |
| POST | `/api/meals/` | 식사기록 생성 | 필요 |
| GET | `/api/meals/{id}/` | 식사기록 단건 조회 | 필요 |
| PUT | `/api/meals/{id}/` | 식사기록 수정 | 필요 |
| DELETE | `/api/meals/{id}/` | 식사기록 삭제 | 필요 |
| GET | `/api/meals/recommend/` | 메뉴 추천 | 필요 |

---

## 📊 ERD

### 테이블 정보

**User (accounts)**
| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | int | PK |
| email | string | 로그인 식별자 (중복 불가) |
| username | string | 유저명 |
| password | string | 해시 저장 |
| is_active | boolean | 계정 활성화 여부 |
| is_staff | boolean | 관리자 여부 |
| created_at | datetime | 생성일시 |
| updated_at | datetime | 수정일시 |

**Meal (meals)**
| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | int | PK |
| menu_name | string | 메뉴명 |
| category | string | 한식/중식/양식/분식/일식 |
| rating | decimal | 평점 (1.0 ~ 5.0) |
| eaten_at | date | 먹은 날짜 |
| owner | int | FK → User |

### 테이블 관계

```
User ————< Meal (1:N)
1명의 유저가 여러 식사 기록 가능
```

---

## 🏗 아키텍처

```
요청
  ↓
urls.py     → URL 라우팅
  ↓
views.py    → 요청/응답 처리
  ↓
serializers.py → 데이터 검증/변환
  ↓
services.py → 비즈니스 로직
  ↓
models.py   → DB 접근
  ↓
응답
```

---

## 💡 구현 포인트

- **역할 분리**: View, Serializer, Service, Model 레이어 분리
- **공통 모듈**: `core` 앱에서 인증, 권한, 예외 공통 관리
- **커스텀 예외**: 401, 403, 404 상황별 예외 처리
- **JWT 인증**: Access Token + Refresh Token 발급
- **Docker**: PostgreSQL + Django 컨테이너 구성
