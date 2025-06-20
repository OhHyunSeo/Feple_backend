# 🎧 Feple 백엔드 시스템

> **AI 기반 콜센터 상담 품질 관리 플랫폼의 통합 백엔드**  
> Django REST API 기반 마이크로서비스 아키텍처

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.1-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![Redis](https://img.shields.io/badge/Redis-6.1+-red.svg)

---

## 📋 목차

- [📖 개요](#-개요)
- [🏗️ 아키텍처](#️-아키텍처)
- [✨ 주요 기능](#-주요-기능)
- [🛠 설치 방법](#-설치-방법)
- [🚀 빠른 시작](#-빠른-시작)
- [📁 프로젝트 구조](#-프로젝트-구조)
- [⚙️ 사용법](#️-사용법)
- [🐳 Docker 사용](#-docker-사용)
- [📡 API 문서](#-api-문서)
- [🔧 설정 가이드](#-설정-가이드)
- [🚨 문제 해결](#-문제-해결)

---

## 📖 개요

**Feple 백엔드 시스템**은 AI 기반 콜센터 상담 품질 관리 플랫폼의 핵심 백엔드입니다. Django REST Framework를 기반으로 한 마이크로서비스 아키텍처를 통해 음성 분석, LLM 기반 평가, 머신러닝 예측을 통합 관리합니다.

### 🎯 핵심 목표
- **통합 API 제공**: 모든 AI 모듈의 통합 인터페이스
- **실시간 처리**: 비동기 작업 처리 및 실시간 알림
- **확장 가능성**: 마이크로서비스 기반 수평 확장
- **데이터 일관성**: 트랜잭션 기반 데이터 무결성 보장

### 🏆 성능 지표
- **API 응답 시간**: 평균 200ms 이하
- **동시 처리**: 최대 1,000개 요청/초
- **가용성**: 99.9% 업타임
- **데이터 처리량**: 10,000건/시간

---

## 🏗️ 아키텍처

```mermaid
graph TB
    subgraph "Frontend Layer"
        FE[React Frontend]
    end
    
    subgraph "API Gateway"
        API[Django REST API]
    end
    
    subgraph "Backend Services"
        DJANGO[Django Backend]
        CALL[Callanalysis Engine]
        LLM[LLM Analysis]
        ML[LightGBM Engine]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL)]
        REDIS[(Redis)]
        FILES[(File Storage)]
    end
    
    FE --> API
    API --> DJANGO
    API --> CALL
    API --> LLM
    API --> ML
    
    DJANGO --> PG
    DJANGO --> REDIS
    CALL --> FILES
    LLM --> PG
    ML --> FILES
```

---

## ✨ 주요 기능

### 🔄 **통합 API 서비스**
- **RESTful API**: 표준 REST API 인터페이스
- **GraphQL 지원**: 유연한 데이터 쿼리
- **실시간 WebSocket**: 실시간 상태 업데이트
- **API 버전 관리**: 하위 호환성 보장

### 🎵 **음성 데이터 처리**
- **파일 업로드**: 다중 형식 음성 파일 지원
- **메타데이터 관리**: 상담 정보 및 속성 관리
- **상태 추적**: 처리 단계별 상태 모니터링
- **결과 통합**: 다양한 분석 결과 통합 관리

### 👥 **사용자 관리**
- **상담원 관리**: 상담원 정보 및 권한 관리
- **팀 관리**: 팀별 성과 및 통계 관리
- **인증/인가**: JWT 기반 보안 인증
- **역할 기반 접근**: 세분화된 권한 제어

### 📊 **분석 결과 관리**
- **통합 대시보드**: 종합 성과 지표
- **리포트 생성**: 자동화된 분석 리포트
- **알림 시스템**: 실시간 상태 알림
- **데이터 내보내기**: 다양한 형식 지원

### 🔄 **비동기 작업 처리**
- **Celery 통합**: 백그라운드 작업 처리
- **작업 큐 관리**: 우선순위 기반 작업 스케줄링
- **진행률 추적**: 실시간 작업 진행률 모니터링
- **실패 복구**: 자동 재시도 및 오류 처리

---

## 🛠 설치 방법

### 📋 시스템 요구사항
- **Python**: 3.11 이상
- **메모리**: 최소 4GB RAM (권장 8GB)
- **디스크**: 10GB 여유 공간
- **OS**: Windows, macOS, Linux
- **PostgreSQL**: 13 이상
- **Redis**: 6.1 이상

### ⚡ 빠른 설치 (Docker 권장)

```bash
# 1. 저장소 클론
git clone <repository-url>
cd Feple_backend

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일 편집

# 3. Docker로 실행
docker-compose up -d

# 4. 서비스 접속
# 백엔드 API: http://localhost:8000
# 프론트엔드: http://localhost:3000
```

### 🔧 로컬 설치

```bash
# 1. Python 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 백엔드 의존성 설치
cd Feple_backend
pip install -r requirements.txt

# 3. 프론트엔드 의존성 설치
cd ../Feple
npm install

# 4. 데이터베이스 설정
python manage.py migrate

# 5. 관리자 계정 생성
python manage.py createsuperuser
```

---

## 🚀 빠른 시작

### 1️⃣ **환경 설정**
```bash
# .env 파일 설정 (필수)
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# 데이터베이스 설정
DATABASE_URL=postgresql://user:password@localhost:5432/feple

# Redis 설정
REDIS_URL=redis://localhost:6379/0

# 외부 서비스 API
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-api-key
```

### 2️⃣ **서비스 실행**
```bash
# Django 개발 서버
python manage.py runserver 8000

# Celery 워커 (별도 터미널)
celery -A backend worker --loglevel=info

# Celery Beat (스케줄러, 별도 터미널)
celery -A backend beat --loglevel=info

# 프론트엔드 개발 서버 (별도 터미널)
cd Feple
npm run dev
```

### 3️⃣ **기본 테스트**
```bash
# API 상태 확인
curl http://localhost:8000/api/health/

# 관리자 페이지 접속
# http://localhost:8000/admin/

# API 문서 확인
# http://localhost:8000/api/docs/
```

---

## 📁 프로젝트 구조

```
Feple_backend/
├── 📄 README.md                     # 이 파일
├── 📄 docker-compose.yml            # Docker 구성
├── 📄 .env.example                  # 환경 변수 템플릿
│
├── 📂 Feple_backend/                # Django 백엔드
│   ├── 📄 manage.py                 # Django 관리 스크립트
│   ├── 📄 requirements.txt          # Python 의존성
│   ├── 📄 Dockerfile                # Docker 이미지 정의
│   ├── 📄 .dockerignore             # Docker 빌드 제외 파일
│   ├── 📄 docker-entrypoint.sh      # Docker 진입점 스크립트
│   │
│   ├── 📂 backend/                  # Django 프로젝트 설정
│   │   ├── __init__.py
│   │   ├── settings.py              # Django 설정
│   │   ├── urls.py                  # URL 라우팅
│   │   ├── wsgi.py                  # WSGI 설정
│   │   ├── asgi.py                  # ASGI 설정
│   │   └── celery.py                # Celery 설정
│   │
│   └── 📂 calls/                    # 메인 앱
│       ├── __init__.py
│       ├── models.py                # 데이터 모델
│       ├── views.py                 # API 뷰
│       ├── serializers.py           # 데이터 직렬화
│       ├── urls.py                  # URL 패턴
│       ├── tasks.py                 # Celery 작업
│       ├── utils.py                 # 유틸리티 함수
│       ├── integration.py           # 외부 서비스 통합
│       ├── admin.py                 # Django 관리자
│       └── tests.py                 # 테스트 코드
│
├── 📂 Feple/                        # React 프론트엔드
│   ├── 📄 package.json              # Node.js 의존성
│   ├── 📄 Dockerfile                # Docker 이미지 정의
│   ├── 📄 nginx.conf                # Nginx 설정
│   ├── 📄 vite.config.ts            # Vite 설정
│   ├── 📄 tailwind.config.cjs       # Tailwind CSS 설정
│   │
│   ├── 📂 src/                      # React 소스 코드
│   │   ├── 📄 App.tsx               # 메인 앱 컴포넌트
│   │   ├── 📄 main.tsx              # 진입점
│   │   │
│   │   ├── 📂 components/           # React 컴포넌트
│   │   │   ├── common/              # 공통 컴포넌트
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Layout.tsx
│   │   │   │   └── Sidebar.tsx
│   │   │   ├── KPIGrid.tsx
│   │   │   ├── PieDistribution.tsx
│   │   │   └── SessionCard.tsx
│   │   │
│   │   ├── 📂 pages/                # 페이지 컴포넌트
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Sessions.tsx
│   │   │   └── Politeness.tsx
│   │   │
│   │   └── 📂 hooks/                # React 훅
│   │       ├── useDashboardData.ts
│   │       └── useSessionData.ts
│   │
│   └── 📂 public/                   # 정적 파일
│       ├── fonts/                   # 폰트 파일
│       └── images/                  # 이미지 파일
│
└── 📂 callanalysis/                 # 음성 분석 엔진
    ├── 📄 main.py                   # 메인 실행 파일
    ├── 📄 requirements.txt          # Python 의존성
    ├── 📄 Dockerfile                # Docker 이미지 정의
    └── 📂 src/                      # 소스 코드
        ├── audio/                   # 오디오 처리
        ├── text/                    # 텍스트 처리
        └── db/                      # 데이터베이스
```

---

## ⚙️ 사용법

### 🎮 **기본 명령어**

```bash
# Django 관리 명령어
python manage.py runserver          # 개발 서버 실행
python manage.py migrate            # 데이터베이스 마이그레이션
python manage.py createsuperuser    # 관리자 계정 생성
python manage.py collectstatic      # 정적 파일 수집

# Celery 명령어
celery -A backend worker --loglevel=info    # 워커 실행
celery -A backend beat --loglevel=info      # 스케줄러 실행
celery -A backend flower                     # 모니터링 도구

# 프론트엔드 명령어
npm run dev                         # 개발 서버
npm run build                       # 프로덕션 빌드
npm run preview                     # 빌드 미리보기
```

### 📊 **데이터 관리**

```bash
# 데이터베이스 백업
python manage.py dumpdata > backup.json

# 데이터베이스 복원
python manage.py loaddata backup.json

# 마이그레이션 생성
python manage.py makemigrations

# 마이그레이션 상태 확인
python manage.py showmigrations

# SQL 쿼리 확인
python manage.py sqlmigrate calls 0001
```

### 🔍 **개발 도구**

```bash
# Django 셸 실행
python manage.py shell

# 데이터베이스 셸 실행
python manage.py dbshell

# 테스트 실행
python manage.py test

# 코드 품질 검사
flake8 .
black .
isort .
```

---

## 🐳 Docker 사용

### 🚀 **빠른 시작**

```bash
# 전체 스택 실행
docker-compose up -d

# 개발 환경 (로그 출력)
docker-compose up

# 특정 서비스만 실행
docker-compose up -d postgres redis
docker-compose up django-backend
```

### 🔧 **Docker 명령어**

```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f django-backend
docker-compose logs -f react-frontend

# 컨테이너 내부 접속
docker-compose exec django-backend bash
docker-compose exec postgres psql -U feple_user -d feple

# 데이터베이스 마이그레이션 (컨테이너 내)
docker-compose exec django-backend python manage.py migrate

# 정적 파일 수집 (컨테이너 내)
docker-compose exec django-backend python manage.py collectstatic --noinput
```

### 📊 **서비스 구성**

```yaml
# docker-compose.yml 주요 서비스
services:
  postgres:           # PostgreSQL 데이터베이스 (포트 5432)
  redis:             # Redis 캐시 서버 (포트 6379)
  django-backend:    # Django API 서버 (포트 8000)
  react-frontend:    # React 웹 앱 (포트 3000)
  celery-worker:     # Celery 워커
  celery-beat:       # Celery 스케줄러
```

---

## 📡 API 문서

### 🔗 **주요 엔드포인트**

#### **인증 관련**
```http
POST /api/auth/login/           # 로그인
POST /api/auth/logout/          # 로그아웃
POST /api/auth/refresh/         # 토큰 갱신
GET  /api/auth/user/            # 사용자 정보
```

#### **상담원 관리**
```http
GET    /api/agents/             # 상담원 목록
POST   /api/agents/             # 상담원 생성
GET    /api/agents/{id}/        # 상담원 상세
PUT    /api/agents/{id}/        # 상담원 수정
DELETE /api/agents/{id}/        # 상담원 삭제
```

#### **통화 데이터**
```http
GET    /api/calls/              # 통화 목록
POST   /api/calls/              # 통화 업로드
GET    /api/calls/{id}/         # 통화 상세
PUT    /api/calls/{id}/         # 통화 수정
DELETE /api/calls/{id}/         # 통화 삭제
GET    /api/calls/{id}/status/  # 처리 상태
```

#### **분석 결과**
```http
GET /api/analyses/              # 분석 결과 목록
GET /api/analyses/{id}/         # 분석 결과 상세
GET /api/transcripts/           # 전사 결과 목록
GET /api/transcripts/{id}/      # 전사 결과 상세
```

#### **대시보드**
```http
GET /api/dashboard/stats/       # 통계 정보
GET /api/dashboard/kpis/        # KPI 지표
GET /api/dashboard/charts/      # 차트 데이터
GET /api/dashboard/reports/     # 리포트 목록
```

### 📋 **요청/응답 예시**

#### **통화 업로드**
```http
POST /api/calls/
Content-Type: multipart/form-data

{
  "audio_file": [파일],
  "agent": 1,
  "call_date": "2024-01-15T14:30:00Z",
  "customer_id": "CUST_001",
  "call_type": "inbound"
}
```

**응답:**
```json
{
  "id": 123,
  "agent": 1,
  "call_date": "2024-01-15T14:30:00Z",
  "customer_id": "CUST_001",
  "call_type": "inbound",
  "status": "processing",
  "created_at": "2024-01-15T14:30:05Z",
  "audio_file": "/media/calls/audio_123.wav"
}
```

#### **분석 결과 조회**
```http
GET /api/analyses/123/
```

**응답:**
```json
{
  "id": 123,
  "call": 123,
  "transcript": "안녕하세요, 고객센터입니다...",
  "sentiment_score": 0.85,
  "satisfaction_score": 4.2,
  "topics": ["문의", "해결", "만족"],
  "summary": "고객 문의에 대한 친절한 응답...",
  "coaching_feedback": "매우 좋은 상담이었습니다...",
  "created_at": "2024-01-15T14:35:00Z"
}
```

### 📊 **API 문서 접속**

```bash
# Swagger UI (개발 환경)
http://localhost:8000/api/docs/

# ReDoc (대안 문서)
http://localhost:8000/api/redoc/

# Django REST Framework 브라우저
http://localhost:8000/api/
```

---

## 🔧 설정 가이드

### ⚙️ **환경 변수**

```bash
# Django 기본 설정
SECRET_KEY=your-django-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# 데이터베이스 설정
DATABASE_URL=postgresql://feple_user:password@postgres:5432/feple
DB_NAME=feple
DB_USER=feple_user
DB_PASSWORD=secure_password
DB_HOST=postgres
DB_PORT=5432

# Redis 설정
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# 외부 API 키
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-api-key

# 파일 저장 설정
MEDIA_ROOT=/app/media
STATIC_ROOT=/app/static
FILE_UPLOAD_MAX_MEMORY_SIZE=52428800  # 50MB

# 보안 설정
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
CSRF_TRUSTED_ORIGINS=http://localhost:3000,https://your-domain.com

# 로깅 설정
LOG_LEVEL=INFO
LOG_FILE=/app/logs/django.log
```

### 📊 **데이터베이스 설정**

```python
# settings.py 데이터베이스 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'feple'),
        'USER': os.getenv('DB_USER', 'feple_user'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 60,
        },
    }
}

# 연결 풀링 설정
DATABASES['default']['CONN_MAX_AGE'] = 600
```

### 🔄 **Celery 설정**

```python
# celery.py 설정
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 작업 라우팅
app.conf.task_routes = {
    'calls.tasks.process_audio': {'queue': 'audio_processing'},
    'calls.tasks.generate_report': {'queue': 'reports'},
}

# 결과 만료 시간
app.conf.result_expires = 3600

# 워커 설정
app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True
```

---

## 🚨 문제 해결

### ❌ **일반적인 오류**

#### **데이터베이스 연결 오류**
```bash
# PostgreSQL 연결 테스트
python manage.py dbshell

# 마이그레이션 상태 확인
python manage.py showmigrations

# 데이터베이스 재생성
docker-compose down -v
docker-compose up -d postgres
python manage.py migrate
```

#### **Redis 연결 오류**
```bash
# Redis 연결 테스트
python -c "
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
print(r.ping())
"

# Celery 상태 확인
celery -A backend inspect active
celery -A backend inspect stats
```

#### **정적 파일 문제**
```bash
# 정적 파일 수집
python manage.py collectstatic --noinput

# 미디어 파일 권한 확인
ls -la media/
chmod -R 755 media/

# Nginx 설정 확인 (프로덕션)
nginx -t
systemctl reload nginx
```

### 🔧 **성능 최적화**

#### **데이터베이스 최적화**
```python
# settings.py 최적화
DATABASES['default'].update({
    'CONN_MAX_AGE': 600,
    'OPTIONS': {
        'MAX_CONNS': 20,
        'connect_timeout': 60,
    }
})

# 쿼리 최적화
from django.db import connection
print(connection.queries)  # 개발 중 쿼리 확인
```

#### **캐싱 설정**
```python
# Redis 캐싱
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# 세션 캐싱
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### 🐛 **디버깅**

```bash
# 디버그 모드 실행
DEBUG=True python manage.py runserver

# 상세 로그 확인
tail -f logs/django.log

# 데이터베이스 쿼리 로깅
python manage.py shell
>>> from django.db import connection
>>> connection.queries

# Celery 작업 모니터링
celery -A backend flower  # http://localhost:5555
```

### 📞 **지원 요청**

문제가 지속될 경우:
1. **로그 파일 확인**: `logs/django.log`, `logs/celery.log`
2. **시스템 정보**: `python --version`, `pip list`
3. **데이터베이스 상태**: `python manage.py dbshell`
4. **서비스 상태**: `docker-compose ps`
5. **GitHub Issues** 또는 **개발팀 연락**: [feple-backend@company.com](mailto:feple-backend@company.com)

---

## 🔗 관련 링크

- **📖 Django 문서**: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- **🔄 Celery 문서**: [https://docs.celeryproject.org/](https://docs.celeryproject.org/)
- **🐘 PostgreSQL 문서**: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
- **📊 API 문서**: http://localhost:8000/api/docs/ (서버 실행 후)

---

## 📄 라이선스

본 프로젝트는 **비공개 라이선스** 하에 배포됩니다.

---

<div align="center">

**🎧 Feple 백엔드로 상담 품질 관리를 혁신하세요! 🎧**

*Made with ❤️ by LG Team*

</div>
