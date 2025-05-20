
# 🎧 Feple 백엔드 시스템

**Feple**은 고객 상담 통화를 AI로 분석하고, 상담원에게 맞춤형 코칭을 제공하는 **지능형 상담 지원 플랫폼**입니다.  
오디오 파일 업로드부터 전사, 감정 분석, 만족도 평가, 그리고 AI 기반 코칭까지 **엔드-투-엔드 자동화**된 백엔드 시스템을 제공합니다.

## 📁 프로젝트 구조

```
FP_back_01/
├── Feple_backend/     # Django 기반 백엔드 API 서버
├── callanalysis/      # 음성 분석 모듈 (STT, 감정 분석 등)
└── Feple/             # 보조 유틸리티 및 기타 코드
```

## 🧰 사용 기술 스택

### 📦 Backend  
<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/DRF-red?style=flat&logo=django&logoColor=white" alt="Django REST Framework"/>
  <img src="https://img.shields.io/badge/Celery-37814A?style=flat&logo=celery&logoColor=white" alt="Celery"/>
  <img src="https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
</p>

### 🧪 Analysis  
<p>
  <img src="https://img.shields.io/badge/Whisper-black?style=flat&logo=whisper&logoColor=white" alt="Whisper"/>
  <img src="https://img.shields.io/badge/SpeechRecognition-FF4088?style=flat" alt="SpeechRecognition"/>
  <img src="https://img.shields.io/badge/pyannote.audio-4B8BBE?style=flat" alt="pyannote"/>
  <img src="https://img.shields.io/badge/transformers-FFB300?style=flat&logo=huggingface&logoColor=white" alt="Transformers"/>
</p>

### 🤖 AI Integration  
<p>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white" alt="OpenAI"/>
</p>

### 🛠 Tools  
<p>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white" alt="Git"/>
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white" alt="GitHub"/>
</p>

## 🧠 주요 모듈 설명

### 1. `Feple_backend` - Django API 서버

- 사용자 인증 및 권한 관리
- 상담원 및 통화 데이터 관리
- 오디오 파일 업로드 및 저장
- `callanalysis` 모듈과 연동
- 분석 결과 저장 및 API 제공
- 비동기 작업 처리 (Celery, Redis)

### 2. `callanalysis` - 음성 분석 엔진

- 음성 → 텍스트 변환 (STT)
- 화자 분리 (Speaker Diarization)
- 감정 분석 및 키워드 추출
- 침묵률, 말 비율 등 통계 계산

## 🚀 핵심 기능

| 기능 항목        | 상세 설명 |
|------------------|-----------|
| 오디오 파일 처리 | REST API 기반 업로드, 상태 추적, 메타데이터 관리 |
| 통화 분석        | 화자 분리, 감정 분석, 요약, 상호작용 평가 |
| 자동 코칭        | OpenAI API 기반 상담원 피드백 생성 |
| 대시보드 지원    | 성과 지표, 만족도 추세, 주요 토픽 시각화 |

## 🧾 주요 데이터 모델

- **Agent**: 상담원 정보
- **CallRawData**: 오디오 파일 및 원본 통화 데이터
- **CallTranscript**: 전사 데이터 및 화자 구분 정보
- **CallAnalysis**: 분석 결과 (감정, 만족도, 토픽 등)
- **AgentCoaching**: AI 기반 상담원 피드백
- **ProcessingTask**: 비동기 처리 모니터링

## 🔌 REST API 요약

| 엔드포인트 | 기능 |
|------------|------|
| `/api/agents/` | 상담원 CRUD |
| `/api/calls/` | 통화 업로드 및 관리 |
| `/api/transcripts/` | 전사 데이터 조회 |
| `/api/analyses/` | 분석 결과 조회 |
| `/api/coaching/` | AI 코칭 피드백 |
| `/api/dashboard/` | 통계 및 대시보드 데이터 |

## 🛠️ 설치 및 실행

### 1. 환경 요구사항

- Python 3.11+
- Redis 서버 (Celery용)
- `.env` 설정 필요 (예: OpenAI API Key)

### 2. 프로젝트 초기화

```bash
# 가상 환경 구성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Django 백엔드 설치
cd Feple_backend
pip install -r requirements.txt
```

`.env` 예시:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your_openai_api_key
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

```bash
# DB 마이그레이션 및 관리자 계정 생성
python manage.py migrate
python manage.py createsuperuser
```

### 3. callanalysis 설치

```bash
cd callanalysis
pip install -r requirements.txt
# (필요한 경우 환경 변수 설정)
```

### 4. 실행 방법

```bash
# Redis 실행
redis-server

# Django 개발 서버 실행
cd Feple_backend
python manage.py runserver

# Celery 워커 실행
celery -A backend worker --loglevel=info

# Celery Beat 실행 (주기적 작업용)
celery -A backend beat --loglevel=info
```

## 🧪 테스트 가이드

### ▶️ API 테스트

테스트용 오디오 파일을 업로드하려면:

```bash
curl -X POST \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -F "audio_file=@/path/to/sample.mp3" \
  -F "agent=1" \
  -F "call_date=2023-08-01T14:30:00" \
  http://localhost:8000/api/calls/
```

상태 확인:
```bash
GET /api/calls/{id}/status/
```

### ▶️ 개발용 테스트 모드

- `Feple_backend/calls/integration.py` 내 테스트 플래그를 설정하면, callanalysis 없이 백엔드 단독으로 테스트 가능

## 📄 라이선스

본 프로젝트는 **비공개 라이선스** 하에 배포됩니다. 무단 사용을 금합니다.
