"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework import routers
from calls.views import (
    AgentViewSet, CallRawDataViewSet, CallTranscriptViewSet,
    CallAnalysisViewSet, AgentCoachingViewSet, DashboardViewSet
)

# API 라우터 설정
router = routers.DefaultRouter()
router.register(r'agents', AgentViewSet)
router.register(r'calls', CallRawDataViewSet)
router.register(r'transcripts', CallTranscriptViewSet)
router.register(r'analyses', CallAnalysisViewSet)
router.register(r'coaching', AgentCoachingViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # 헬스 체크 엔드포인트
    path('health/', include('health_check.urls')),
    
    # 단수형 URL 리다이렉트 (사용자 편의성)
    path('api/agent/', RedirectView.as_view(url='/api/agents/', permanent=False)),
    path('api/call/', RedirectView.as_view(url='/api/calls/', permanent=False)),
    path('api/transcript/', RedirectView.as_view(url='/api/transcripts/', permanent=False)),
    path('api/analysis/', RedirectView.as_view(url='/api/analyses/', permanent=False)),
    
    # 루트 URL 리다이렉트
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
]

# 개발 환경에서 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
