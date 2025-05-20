import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from django.conf import settings

logger = logging.getLogger('calls')


def get_callanalysis_path():
    """callanalysis 프로젝트 경로 반환"""
    # 상대 경로 사용 (백엔드와 callanalysis가 같은 디렉토리에 있다고 가정)
    callanalysis_path = os.path.join(settings.BASE_DIR.parent, 'callanalysis')
    return callanalysis_path


def call_callanalysis_process(audio_file_path):
    """
    callanalysis의 main.py 스크립트를 호출하여 오디오 파일 처리
    
    Parameters
    ----------
    audio_file_path : str
        처리할 오디오 파일 경로
        
    Returns
    -------
    dict or None
        처리 결과 데이터 (성공 시) 또는 None (실패 시)
    """
    # 원래 코드를 주석 처리하고 테스트용 더미 데이터 반환
    logger.info(f"[테스트 모드] 더미 데이터 반환 (실제 callanalysis 호출 없음): {audio_file_path}")
    
    # 테스트용 더미 데이터
    dummy_result = {
        "transcript": "안녕하세요. 무엇을 도와드릴까요? 저는 기타 관련해서 문의가 있어요. 싼 기타와 비싼 기타의 차이점이 궁금합니다. 네, 비싼 기타는 소리 품질이 더 좋고 내구성이 뛰어납니다. 또한 목재의 품질과 제작 기술이 다릅니다. 그렇군요. 초보자에게는 어떤 기타가 좋을까요? 초보자에게는 중저가 기타를 추천해 드립니다. 연습용으로 충분하고 나중에 실력이 늘면 업그레이드할 수 있어요. 알겠습니다. 감사합니다. 다른 문의사항 있으신가요? 아니요, 충분히 도움이 되었습니다. 감사합니다. 감사합니다. 좋은 하루 되세요.",
        "speaker_timestamps": {
            "speakers": [
                {"id": "AGENT", "utterances": [
                    {"start": 0.0, "end": 4.5, "text": "안녕하세요. 무엇을 도와드릴까요?"},
                    {"start": 13.2, "end": 29.8, "text": "네, 비싼 기타는 소리 품질이 더 좋고 내구성이 뛰어납니다. 또한 목재의 품질과 제작 기술이 다릅니다."},
                    {"start": 38.0, "end": 55.3, "text": "초보자에게는 중저가 기타를 추천해 드립니다. 연습용으로 충분하고 나중에 실력이 늘면 업그레이드할 수 있어요."},
                    {"start": 63.8, "end": 68.2, "text": "다른 문의사항 있으신가요?"},
                    {"start": 75.0, "end": 78.5, "text": "감사합니다. 좋은 하루 되세요."}
                ]},
                {"id": "CUSTOMER", "utterances": [
                    {"start": 5.0, "end": 12.7, "text": "저는 기타 관련해서 문의가 있어요. 싼 기타와 비싼 기타의 차이점이 궁금합니다."},
                    {"start": 30.5, "end": 37.5, "text": "그렇군요. 초보자에게는 어떤 기타가 좋을까요?"},
                    {"start": 56.0, "end": 62.3, "text": "알겠습니다. 감사합니다."},
                    {"start": 69.0, "end": 74.5, "text": "아니요, 충분히 도움이 되었습니다. 감사합니다."}
                ]}
            ]
        },
        "audio_stats": {
            "duration": 80.0,
            "silence_rate": 0.15,
            "agent_talk_ratio": 0.65,
            "customer_talk_ratio": 0.35,
            "interruption_count": 0
        },
        "sentiment": {
            "agent": {"positive": 0.8, "neutral": 0.15, "negative": 0.05},
            "customer": {"positive": 0.7, "neutral": 0.25, "negative": 0.05}
        }
    }
    
    return dummy_result
    
    # 기존 코드 (주석 처리)
    """
    callanalysis_path = get_callanalysis_path()
    logger.info(f"Calling callanalysis process with audio file: {audio_file_path}")
    
    try:
        # subprocess로 callanalysis 호출
        process = subprocess.Popen(
            [sys.executable, 'main.py', audio_file_path],
            cwd=callanalysis_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            logger.error(f"Error running callanalysis: {stderr}")
            return None
        
        # 출력에서 JSON 결과 추출 (결과가 파일로 저장된 경우)
        output_json_path = os.path.join(callanalysis_path, '.temp', 'output.json')
        if os.path.exists(output_json_path):
            with open(output_json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        # 직접 출력에서 JSON 파싱 시도
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            logger.error("Could not parse JSON from callanalysis output")
            
        return None
            
    except Exception as e:
        logger.exception(f"Exception calling callanalysis: {str(e)}")
        return None
    """


def extract_transcript_data(callanalysis_result):
    """
    callanalysis 결과에서 전사 데이터 추출
    
    Parameters
    ----------
    callanalysis_result : dict
        callanalysis 처리 결과
    
    Returns
    -------
    tuple
        (전체 전사 텍스트, 화자 분리 데이터, 침묵률)
    """
    try:
        # 샘플 데이터 구조에 맞춰 파싱
        # 실제 callanalysis 결과 구조에 맞게 수정 필요
        transcript = callanalysis_result.get('transcript', '')
        speakers_data = callanalysis_result.get('speaker_timestamps', {})
        silence_rate = callanalysis_result.get('audio_stats', {}).get('silence_rate', 0.0)
        
        return transcript, speakers_data, silence_rate
    except Exception as e:
        logger.exception(f"Error extracting transcript data: {str(e)}")
        # 기본값 반환
        return "", {}, 0.0


def call_lightgbm_model(features):
    """
    LightGBM 모델을 사용하여 만족도 예측
    
    Parameters
    ----------
    features : dict
        예측에 사용할 특성 데이터
    
    Returns
    -------
    tuple
        (만족도 점수, 카테고리) - 실패 시 기본값 반환
    """
    try:
        # 실제 구현에서는 모델 로드 및 예측
        import joblib
        import numpy as np
        
        # 모델 경로
        model_path = os.path.join(settings.BASE_DIR, 'calls', 'models', 'lightgbm_model.pkl')
        
        # 모델 파일이 있는지 확인
        if not os.path.exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            return 3.0, "보통"  # 기본값
        
        # 모델 로드
        model = joblib.load(model_path)
        
        # 특성 변환
        feature_array = np.array([
            features.get('silence_rate', 0.0),
            features.get('agent_talk_ratio', 0.5),
            features.get('interruption_count', 0),
            features.get('avg_response_time', 1.0),
            # 필요한 다른 특성들...
        ]).reshape(1, -1)
        
        # 예측
        score = float(model.predict(feature_array)[0])
        
        # 카테고리 매핑
        if score < 2.0:
            category = "낮음"
        elif score < 4.0:
            category = "보통"
        else:
            category = "높음"
            
        return score, category
        
    except Exception as e:
        logger.exception(f"Error predicting satisfaction: {str(e)}")
        return 3.0, "보통"  # 기본값


def call_openai_for_evaluation(transcript, speakers_data, agent_name):
    """
    OpenAI API를 사용하여 통화 내용 평가
    
    Parameters
    ----------
    transcript : str
        전체 전사 텍스트
    speakers_data : dict
        화자 분리 데이터
    agent_name : str
        상담원 이름
    
    Returns
    -------
    tuple
        (평가 텍스트, 평가 점수, 주요 토픽, 감정 데이터, 요약)
    """
    try:
        import openai
        from openai import OpenAI
        from .utils import format_conversation_for_llm
        
        # API 키 설정
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            return generate_fallback_evaluation(agent_name)
            
        # 대화 포맷팅
        formatted_conversation = format_conversation_for_llm(speakers_data)
        
        # 클라이언트 초기화
        client = OpenAI(api_key=api_key)
        
        # 평가 요청
        evaluation_prompt = f"""
        다음은 고객 상담 대화입니다:
        
        {formatted_conversation}
        
        상담원 {agent_name}의 응대를 다음 기준으로 평가해주세요:
        1. 전반적인 평가와 점수 (1-5)
        2. 주요 대화 주제 (3개 이내)
        3. 화자별 감정 분석
        4. 통화 내용 요약 (1-2문장)
        
        다음 JSON 형식으로 결과를 반환해주세요:
        {{
            "evaluation": "평가 내용",
            "score": 4.5,
            "topics": ["주제1", "주제2", "주제3"],
            "emotions": {{"agent": "감정", "customer": "감정"}},
            "summary": "통화 요약"
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "고객 상담 평가 전문가로서 응답해주세요. JSON 형식을 정확히 따라주세요."},
                {"role": "user", "content": evaluation_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # 응답 파싱
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        
        # 결과 추출
        evaluation = result.get("evaluation", "평가 정보 없음")
        score = result.get("score", 3.0)
        topics = result.get("topics", [])
        emotions = result.get("emotions", {})
        summary = result.get("summary", "요약 정보 없음")
        
        return evaluation, score, topics, emotions, summary
        
    except Exception as e:
        logger.exception(f"Error calling OpenAI API: {str(e)}")
        return generate_fallback_evaluation(agent_name)


def generate_fallback_evaluation(agent_name):
    """
    OpenAI API 호출 실패 시 기본 평가 결과 생성
    
    Parameters
    ----------
    agent_name : str
        상담원 이름
    
    Returns
    -------
    tuple
        (평가 텍스트, 평가 점수, 주요 토픽, 감정 데이터, 요약)
    """
    return (
        f"{agent_name} 상담원의 상담에 대한 평가를 생성할 수 없습니다.",
        3.0,
        ["기타"],
        {"agent": "중립", "customer": "중립"},
        "상담 내용 요약을 생성할 수 없습니다."
    )


def generate_daily_coaching(agent_name, date, call_summaries, avg_satisfaction):
    """
    상담원 일일 코칭 데이터 생성
    
    Parameters
    ----------
    agent_name : str
        상담원 이름
    date : date
        날짜
    call_summaries : list
        통화 요약 목록
    avg_satisfaction : float
        평균 만족도 점수
    
    Returns
    -------
    dict
        코칭 데이터
    """
    try:
        import openai
        from openai import OpenAI
        
        # API 키 설정
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            return generate_fallback_coaching(agent_name, len(call_summaries), avg_satisfaction)
            
        # 클라이언트 초기화
        client = OpenAI(api_key=api_key)
        
        # 요약 정보 가공
        summaries_text = "\n".join([f"- {summary}" for summary in call_summaries])
        
        # 코칭 요청
        coaching_prompt = f"""
        상담원 {agent_name}의 {date.strftime('%Y-%m-%d')} 상담 내용 요약:
        
        {summaries_text}
        
        통화 수: {len(call_summaries)}
        평균 만족도: {avg_satisfaction:.1f}/5.0
        
        위 정보를 바탕으로 상담원을 위한 코칭 내용을 생성해주세요. 다음 JSON 형식으로 결과를 반환해주세요:
        
        {{
            "summary": "하루 상담 요약",
            "coaching_points": "코칭 포인트",
            "strengths": "강점",
            "areas_to_improve": "개선점"
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 고객 상담 코칭 전문가입니다. JSON 형식을 정확히 따라주세요."},
                {"role": "user", "content": coaching_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # 응답 파싱
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        
        # 결과 추출 및 반환
        return {
            "summary": result.get("summary", "요약 정보 없음"),
            "coaching_points": result.get("coaching_points", "코칭 포인트 없음"),
            "strengths": result.get("strengths", "강점 정보 없음"),
            "areas_to_improve": result.get("areas_to_improve", "개선점 정보 없음")
        }
        
    except Exception as e:
        logger.exception(f"Error generating coaching: {str(e)}")
        return generate_fallback_coaching(agent_name, len(call_summaries), avg_satisfaction)


def generate_fallback_coaching(agent_name, call_count, avg_satisfaction):
    """
    코칭 생성 실패 시 기본 코칭 데이터 생성
    
    Parameters
    ----------
    agent_name : str
        상담원 이름
    call_count : int
        통화 수
    avg_satisfaction : float
        평균 만족도 점수
    
    Returns
    -------
    dict
        기본 코칭 데이터
    """
    return {
        "summary": f"{agent_name} 상담원은 오늘 총 {call_count}건의 상담을 진행하였으며, 평균 만족도는 {avg_satisfaction:.1f}점입니다.",
        "coaching_points": "시스템 오류로 인해 코칭 포인트를 생성할 수 없습니다.",
        "strengths": "강점 정보를 생성할 수 없습니다.",
        "areas_to_improve": "개선점 정보를 생성할 수 없습니다."
    } 