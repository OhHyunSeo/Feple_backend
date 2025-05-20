from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import date

from .models import (
    Agent, CallRawData, CallTranscript, 
    CallAnalysis, AgentCoaching, ProcessingTask
)
from .serializers import (
    AgentSerializer, CallRawDataSerializer, CallTranscriptSerializer,
    CallAnalysisSerializer, AgentCoachingSerializer, ProcessingTaskSerializer,
    CallDetailSerializer
)
from .tasks import process_call, daily_coaching


class AgentViewSet(viewsets.ModelViewSet):
    """상담원 관련 API 엔드포인트"""
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def calls(self, request, pk=None):
        """특정 상담원의 통화 목록 조회"""
        agent = self.get_object()
        calls = CallRawData.objects.filter(agent=agent)
        
        # 필터링
        status_filter = request.query_params.get('status', None)
        if status_filter:
            calls = calls.filter(status=status_filter)
            
        # 날짜 필터링
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date:
            calls = calls.filter(call_date__gte=start_date)
        if end_date:
            calls = calls.filter(call_date__lte=end_date)
            
        page = self.paginate_queryset(calls)
        serializer = CallRawDataSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'])
    def coaching(self, request, pk=None):
        """특정 상담원의 코칭 기록 조회"""
        agent = self.get_object()
        coaching = AgentCoaching.objects.filter(agent=agent)
        
        # 날짜 필터링
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date:
            coaching = coaching.filter(date__gte=start_date)
        if end_date:
            coaching = coaching.filter(date__lte=end_date)
            
        page = self.paginate_queryset(coaching)
        serializer = AgentCoachingSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """특정 상담원의 통계 데이터 조회"""
        agent = self.get_object()
        
        # 기간별 통계 (기본값: 오늘)
        start_date = request.query_params.get('start_date', date.today().isoformat())
        end_date = request.query_params.get('end_date', date.today().isoformat())
        
        # 통화 통계
        calls = CallRawData.objects.filter(
            agent=agent,
            call_date__date__gte=start_date,
            call_date__date__lte=end_date
        )
        
        # 분석 데이터가 있는 통화만 필터링
        analyzed_calls = calls.filter(analysis__isnull=False)
        
        stats = {
            'call_count': calls.count(),
            'avg_satisfaction': analyzed_calls.aggregate(
                avg_score=Avg('analysis__satisfaction_score')
            )['avg_score'],
            'completed_calls': calls.filter(status='completed').count(),
            'pending_calls': calls.filter(status='pending').count(),
            'processing_calls': calls.filter(status='processing').count(),
            'avg_call_duration': calls.aggregate(
                avg_duration=Avg('duration')
            )['avg_duration'],
            'period': {
                'start_date': start_date,
                'end_date': end_date,
            }
        }
        
        return Response(stats)


class CallRawDataViewSet(viewsets.ModelViewSet):
    """통화 데이터 API 엔드포인트"""
    queryset = CallRawData.objects.all()
    serializer_class = CallRawDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CallDetailSerializer
        return CallRawDataSerializer

    def perform_create(self, serializer):
        """통화 업로드 시 Celery 태스크 트리거"""
        call_instance = serializer.save()
        
        # 상태 업데이트
        call_instance.status = 'processing'
        call_instance.save()
        
        # 태스크 생성 및 트리거
        task = ProcessingTask.objects.create(
            call=call_instance,
            agent=call_instance.agent,
            task_type='transcription',
            status='pending'
        )
        
        # Celery 태스크 시작
        result = process_call.delay(call_instance.id)
        
        # 태스크 ID 저장
        task.task_id = result.id
        task.status = 'processing'
        task.save()

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """특정 통화의 처리 상태 조회"""
        call = self.get_object()
        tasks = ProcessingTask.objects.filter(call=call)
        
        result = {
            'id': call.id,
            'status': call.status,
            'tasks': ProcessingTaskSerializer(tasks, many=True).data
        }
        
        # 분석 결과가 있는 경우 포함
        if hasattr(call, 'analysis'):
            result['analysis'] = CallAnalysisSerializer(call.analysis).data
            
        # 전사 결과가 있는 경우 포함
        if hasattr(call, 'transcript'):
            result['transcript'] = {
                'id': call.transcript.id,
                'silence_rate': call.transcript.silence_rate
            }
            
        return Response(result)
    
    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        """특정 통화 재처리 요청"""
        call = self.get_object()
        
        # 이미 처리 중인 태스크가 있는 경우
        if ProcessingTask.objects.filter(call=call, status='processing').exists():
            return Response(
                {'error': '이미 처리 중인 작업이 있습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 상태 업데이트
        call.status = 'processing'
        call.save()
        
        # 새 태스크 생성
        task = ProcessingTask.objects.create(
            call=call,
            agent=call.agent,
            task_type='transcription',
            status='pending'
        )
        
        # Celery 태스크 시작
        result = process_call.delay(call.id)
        
        # 태스크 ID 저장
        task.task_id = result.id
        task.status = 'processing'
        task.save()
        
        return Response({'task_id': result.id, 'status': 'processing'})


class CallTranscriptViewSet(viewsets.ReadOnlyModelViewSet):
    """통화 전사 데이터 API 엔드포인트 (읽기 전용)"""
    queryset = CallTranscript.objects.all()
    serializer_class = CallTranscriptSerializer
    permission_classes = [permissions.IsAuthenticated]


class CallAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """통화 분석 결과 API 엔드포인트 (읽기 전용)"""
    queryset = CallAnalysis.objects.all()
    serializer_class = CallAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]


class AgentCoachingViewSet(viewsets.ReadOnlyModelViewSet):
    """상담원 코칭 API 엔드포인트 (읽기 전용)"""
    queryset = AgentCoaching.objects.all()
    serializer_class = AgentCoachingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def generate_today(self, request):
        """오늘 날짜의 코칭 데이터 생성 요청"""
        agent_id = request.data.get('agent_id')
        if not agent_id:
            return Response(
                {'error': '상담원 ID가 필요합니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        agent = get_object_or_404(Agent, id=agent_id)
        
        # 이미 오늘 코칭이 생성되었는지 확인
        today = date.today()
        existing = AgentCoaching.objects.filter(agent=agent, date=today).first()
        if existing:
            return Response(
                {'error': '이미 오늘의 코칭이 생성되었습니다.', 'coaching_id': existing.id},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 비동기 태스크 생성
        task = ProcessingTask.objects.create(
            agent=agent,
            task_type='coaching',
            status='pending'
        )
        
        # Celery 태스크 시작
        result = daily_coaching.delay(agent.id, today.isoformat())
        
        # 태스크 ID 저장
        task.task_id = result.id
        task.status = 'processing'
        task.save()
        
        return Response({'task_id': result.id, 'status': 'processing'})


class DashboardViewSet(viewsets.ViewSet):
    """대시보드 데이터 API 엔드포인트"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """대시보드 개요 데이터"""
        # 기간 필터
        days = int(request.query_params.get('days', 7))  # 기본값 7일
        
        # 기준 날짜
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=days)
        
        # 통화 통계
        calls = CallRawData.objects.filter(
            call_date__gte=start_date,
            call_date__lte=end_date
        )
        
        # 분석된 통화
        analyzed_calls = calls.filter(analysis__isnull=False)
        
        # 상담원별 통계
        agent_stats = Agent.objects.annotate(
            call_count=Count('calls', filter=models.Q(calls__call_date__gte=start_date, calls__call_date__lte=end_date)),
            avg_satisfaction=Avg('calls__analysis__satisfaction_score', filter=models.Q(calls__call_date__gte=start_date, calls__call_date__lte=end_date))
        )
        
        # 통계 데이터
        stats = {
            'total_calls': calls.count(),
            'completed_analysis': analyzed_calls.count(),
            'avg_satisfaction': analyzed_calls.aggregate(avg=Avg('analysis__satisfaction_score'))['avg'],
            'agents': {
                'total': agent_stats.count(),
                'top_performers': AgentSerializer(
                    agent_stats.order_by('-avg_satisfaction')[:3], 
                    many=True
                ).data
            },
            'period': {
                'start_date': start_date,
                'end_date': end_date,
                'days': days
            }
        }
        
        return Response(stats)
