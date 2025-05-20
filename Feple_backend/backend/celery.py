import os
from celery import Celery
from django.conf import settings

# Django settings 모듈 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Celery 앱 생성
app = Celery('backend')

# settings.py에서 CELERY로 시작하는 설정 값들을 사용
app.config_from_object('django.conf:settings', namespace='CELERY')

# 등록된 Django 앱에서 tasks.py 모듈 자동 탐색
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 