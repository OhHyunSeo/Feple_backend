# Feple 백엔드 시스템

Feple 백엔드 시스템은 고객 상담 통화를 분석하고 상담원에게 코칭을 제공하는 종합 솔루션입니다. 이 시스템은 오디오 파일 업로드, 음성 전사, 화자 분리, 감정 분석, 만족도 평가 및 AI 기반 코칭 기능을 제공합니다.

## 프로젝트 구조

프로젝트는 두 개의 주요 모듈로 구성되어 있습니다:

```
FP_back_01/
├── Feple_backend/     # Django 백엔드 애플리케이션
├── callanalysis/      # 통화 분석 모듈
└── Feple/             # 기타 관련 코드
```

### Feple_backend (Django 애플리케이션)

Django 기반 RESTful API 서버로, 다음 기능을 제공합니다:

- 사용자 인증 및 권한 관리
- 상담원 및 통화 데이터 관리
- 통화 녹음 파일 업로드 및 저장
- callanalysis 모듈과의 연동
- 분석 결과 및 코칭 데이터 저장 및 API 제공
- 비동기 작업 처리 (Celery)

### callanalysis (통화 분석 모듈)

Python 기반 음성 분석 모듈로, 다음 기능을 제공합니다:

- 음성 전사 (Speech-to-Text)
- 화자 분리 (Speaker Diarization)
- 감정 분석 및 토픽 추출
- 통화 통계 생성 (침묵률, 대화 비율 등)

## 주요 기능

1. **오디오 파일 업로드 및 관리**
   - REST API를 통한 오디오 파일 업로드
   - 파일 메타데이터 관리 및 상태 추적

2. **통화 분석**
   - 음성 텍스트 변환 및 화자 분리
   - 통화 내용 분석 및 요약
   - 상담원-고객 상호작용 평가

3. **상담원 코칭**
   - OpenAI API 기반 자동화된 코칭 생성
   - 강점 및 개선점 식별
   - 일일 성과 요약 및 코칭 포인트 제공

4. **대시보드 및 통계**
   - 상담원 성과 지표
   - 만족도 추세 분석
   - 통화 패턴 및 주요 토픽 분석

## 데이터 모델

주요 데이터 모델:

- **Agent**: 상담원 정보
- **CallRawData**: 원본 통화 데이터 및 오디오 파일
- **CallTranscript**: 통화 전사 데이터 및 화자 분리 정보
- **CallAnalysis**: 통화 분석 결과 (만족도, 감정, 주요 토픽)
- **AgentCoaching**: 상담원 코칭 정보
- **ProcessingTask**: 비동기 작업 모니터링

## API 엔드포인트

주요 API 엔드포인트:

- `/api/agents/` - 상담원 관리
- `/api/calls/` - 통화 데이터 관리 및 오디오 파일 업로드
- `/api/transcripts/` - 통화 전사 데이터 조회
- `/api/analyses/` - 통화 분석 결과 조회
- `/api/coaching/` - 상담원 코칭 데이터 관리
- `/api/dashboard/` - 대시보드 데이터 제공

## 설치 및 설정

### 사전 요구사항

- Python 3.11 이상
- Redis (Celery 메시지 브로커)
- 충분한 디스크 공간 (오디오 파일 저장용)

### 백엔드 설정

1. 가상 환경 생성 및 활성화
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. 의존성 패키지 설치
   ```bash
   cd Feple_backend
   pip install -r requirements.txt
   ```

3. 환경 변수 설정 (.env 파일 생성)
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   OPENAI_API_KEY=your_openai_api_key
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```

4. 데이터베이스 마이그레이션
   ```bash
   python manage.py migrate
   ```

5. 관리자 계정 생성
   ```bash
   python manage.py createsuperuser
   ```

### callanalysis 설정

1. 의존성 패키지 설치
   ```bash
   cd callanalysis
   pip install -r requirements.txt
   ```

2. 필요한 환경 변수 설정

## 실행 방법

1. Redis 서버 실행
   ```bash
   redis-server
   ```

2. Django 서버 실행
   ```bash
   cd Feple_backend
   python manage.py runserver
   ```

3. Celery 워커 실행
   ```bash
   cd Feple_backend
   celery -A backend worker --loglevel=info
   ```

4. Celery Beat 실행 (스케줄링된 작업용)
   ```bash
   cd Feple_backend
   celery -A backend beat --loglevel=info
   ```

## 테스트 방법

### 테스트 모드로 실행

callanalysis 모듈 없이 Django 백엔드만 테스트하려면:

1. `Feple_backend/calls/integration.py` 파일이 테스트 모드로 설정되어 있는지 확인
2. Django 서버와 Celery 워커 실행
3. 관리자 페이지(`/admin/`)에서 테스트 데이터 생성 또는 API를 통해 테스트

### 오디오 파일 업로드 테스트

1. 테스트할 오디오 파일을 준비
2. `/api/calls/` 엔드포인트로 POST 요청 전송:
   ```bash
   curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "audio_file=@/경로/파일명.mp3" \
     -F "agent=1" \
     -F "call_date=2023-08-01T14:30:00" \
     http://localhost:8000/api/calls/
   ```
3. 작업 상태를 확인: `/api/calls/{id}/status/`

## 라이선스

이 프로젝트는 비공개 라이선스로 배포됩니다.

## 작성자

Feple 개발팀 