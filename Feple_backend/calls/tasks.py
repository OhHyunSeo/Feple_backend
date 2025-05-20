import os
import logging
import time
from celery import shared_task
from datetime import datetime, date
from django.utils import timezone
from django.db.models import Avg
from django.conf import settings

from .models import (
    CallRawData, CallTranscript, CallAnalysis, 
    AgentCoaching, ProcessingTask, Agent
)
from .integration import (
    call_callanalysis_process, extract_transcript_data, 
    call_lightgbm_model, call_openai_for_evaluation,
    generate_daily_coaching
)
from .utils import get_audio_duration, extract_audio_features, format_conversation_for_llm

logger = logging.getLogger('calls')


@shared_task
def process_call(call_id):
    """오디오 파일 처리 작업"""
    logger.info(f"Processing call {call_id}")
    call_instance = CallRawData.objects.get(id=call_id)
    
    try:
        # 오디오 길이 계산 및 저장 (없는 경우)
        if not call_instance.duration:
            duration = get_audio_duration(call_instance.audio_file.path)
            if duration:
                call_instance.duration = int(duration)
                call_instance.save(update_fields=['duration'])
        
        # 1단계: 전사 서비스 호출 (STT)
        transcription_task = ProcessingTask.objects.filter(
            call=call_instance,
            task_type='transcription'
        ).first()
        
        if transcription_task:
            transcription_task.status = 'processing'
            transcription_task.save()
        
        # callanalysis 호출
        callanalysis_result = call_callanalysis_process(call_instance.audio_file.path)
        if not callanalysis_result:
            raise Exception("Failed to process audio with callanalysis")
            
        # 결과 추출
        transcript, speakers_data, silence_rate = extract_transcript_data(callanalysis_result)
        
        # 전사 결과 저장
        call_transcript = CallTranscript.objects.create(
            call=call_instance,
            full_transcript=transcript,
            speakers_json=speakers_data,
            silence_rate=silence_rate
        )
        
        if transcription_task:
            transcription_task.status = 'completed'
            transcription_task.save()
        
        # 2단계: 만족도 분석 (ML 모델)
        analysis_task = ProcessingTask.objects.create(
            call=call_instance,
            agent=call_instance.agent,
            task_type='analysis',
            status='processing'
        )
        
        # 오디오 특성 추출
        audio_features = extract_audio_features(call_instance.audio_file.path)
        
        # 특성 데이터 준비
        features = {
            'silence_rate': silence_rate,
            # 다른 특성들 추가
        }
        if audio_features:
            features.update(audio_features)
        
        # 모델 호출
        satisfaction_score, satisfaction_category = call_lightgbm_model(features)
        
        # 만족도 분석 결과 저장
        call_analysis = CallAnalysis.objects.create(
            call=call_instance,
            satisfaction_score=satisfaction_score,
            satisfaction_category=satisfaction_category
        )
        
        analysis_task.status = 'completed'
        analysis_task.save()
        
        # 3단계: LLM 평가
        llm_task = ProcessingTask.objects.create(
            call=call_instance,
            agent=call_instance.agent,
            task_type='llm_evaluation',
            status='processing'
        )
        
        llm_evaluation, llm_score, topics, emotions, summary = call_openai_for_evaluation(
            transcript,
            speakers_data,
            call_instance.agent.user.get_full_name()
        )
        
        # LLM 평가 결과 저장
        call_analysis.llm_evaluation = llm_evaluation
        call_analysis.llm_score = llm_score
        call_analysis.key_topics = topics
        call_analysis.emotions = emotions
        call_analysis.summary = summary
        call_analysis.save()
        
        llm_task.status = 'completed'
        llm_task.save()
        
        # 통화 처리 상태 업데이트
        call_instance.status = 'completed'
        call_instance.save()
        
        logger.info(f"Successfully processed call {call_id}")
        return {
            'call_id': call_id,
            'status': 'completed',
            'satisfaction_score': satisfaction_score
        }
        
    except Exception as e:
        # 오류 발생 시 상태 업데이트
        error_msg = str(e)
        logger.error(f"Error processing call {call_id}: {error_msg}")
        
        # 작업 상태 업데이트
        for task in ProcessingTask.objects.filter(
            call=call_instance,
            status='processing'
        ):
            task.status = 'failed'
            task.error_message = error_msg
            task.save()
        
        # 통화 상태 업데이트
        call_instance.status = 'failed'
        call_instance.save()
        
        raise


@shared_task
def daily_coaching(agent_id, target_date=None):
    """상담원 일일 코칭 생성"""
    logger.info(f"Generating daily coaching for agent {agent_id}")
    
    try:
        agent = Agent.objects.get(id=agent_id)
        
        # 날짜 설정
        if target_date:
            coaching_date = datetime.fromisoformat(target_date).date()
        else:
            coaching_date = date.today()
        
        # 해당 날짜의 통화 조회
        calls = CallRawData.objects.filter(
            agent=agent,
            call_date__date=coaching_date,
            status='completed'
        )
        
        # 통화가 없으면 빈 코칭 생성
        if not calls.exists():
            AgentCoaching.objects.create(
                agent=agent,
                date=coaching_date,
                daily_summary="오늘의 통화 데이터가 없습니다.",
                coaching_points="통화 데이터가 충분하지 않아 코칭 포인트를 생성할 수 없습니다.",
                call_count=0
            )
            
            logger.info(f"No calls found for agent {agent_id} on {coaching_date}")
            return {
                'agent_id': agent_id,
                'date': coaching_date.isoformat(),
                'status': 'completed',
                'message': 'No calls found'
            }
        
        # 통화 분석 데이터 수집
        analyzed_calls = calls.filter(analysis__isnull=False)
        call_count = calls.count()
        avg_satisfaction = analyzed_calls.aggregate(avg=Avg('analysis__satisfaction_score'))['avg'] or 3.0
        
        # 요약 정보 수집
        summaries = []
        for call in calls.filter(analysis__isnull=False):
            if call.analysis.summary:
                summaries.append(call.analysis.summary)
        
        # 코칭 내용 생성 (LLM 사용)
        coaching_data = generate_daily_coaching(
            agent.user.get_full_name(),
            coaching_date,
            summaries,
            avg_satisfaction
        )
        
        # 코칭 저장
        coaching = AgentCoaching.objects.create(
            agent=agent,
            date=coaching_date,
            daily_summary=coaching_data['summary'],
            coaching_points=coaching_data['coaching_points'],
            strengths=coaching_data['strengths'],
            areas_to_improve=coaching_data['areas_to_improve'],
            call_count=call_count,
            avg_satisfaction=avg_satisfaction
        )
        
        logger.info(f"Successfully generated coaching for agent {agent_id} on {coaching_date}")
        return {
            'agent_id': agent_id,
            'date': coaching_date.isoformat(),
            'coaching_id': coaching.id,
            'status': 'completed'
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error generating coaching for agent {agent_id}: {error_msg}")
        
        # 작업 상태 업데이트
        for task in ProcessingTask.objects.filter(
            agent_id=agent_id,
            task_type='coaching',
            status='processing'
        ):
            task.status = 'failed'
            task.error_message = error_msg
            task.save()
            
        raise 