import os
import json
import logging
import tempfile
import subprocess
from pathlib import Path
from django.conf import settings

logger = logging.getLogger('calls')


def ensure_directory_exists(directory_path):
    """디렉토리가 존재하지 않으면 생성"""
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def get_audio_duration(file_path):
    """오디오 파일의 재생 시간을 초 단위로 반환"""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0  # 밀리초를 초로 변환
    except Exception as e:
        logger.error(f"Error getting audio duration: {str(e)}")
        return None


def convert_audio_format(input_path, output_format='wav'):
    """오디오 파일을 다른 포맷으로 변환"""
    try:
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(tempfile.gettempdir(), f"{name}.{output_format}")
        
        from pydub import AudioSegment
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=output_format)
        
        return output_path
    except Exception as e:
        logger.error(f"Error converting audio format: {str(e)}")
        return None


def extract_audio_features(file_path):
    """오디오 파일에서 특성 추출 (침묵 비율, 볼륨 등)"""
    try:
        # 웨이브 파일로 변환
        wav_path = convert_audio_format(file_path, 'wav')
        if not wav_path:
            return None
            
        # librosa 사용하여 특성 추출
        import librosa
        import numpy as np
        
        y, sr = librosa.load(wav_path)
        
        # 특성 계산
        rms = librosa.feature.rms(y=y)[0]
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # 침묵 감지
        non_silent_intervals = librosa.effects.split(y, top_db=20)
        total_duration = len(y) / sr
        silence_duration = total_duration - sum([(end - start) / sr for start, end in non_silent_intervals])
        silence_ratio = (silence_duration / total_duration) * 100
        
        features = {
            'rms_mean': float(np.mean(rms)),
            'zcr_mean': float(np.mean(zcr)),
            'spectral_centroid_mean': float(np.mean(spectral_centroid)),
            'mfccs': [float(np.mean(mfcc)) for mfcc in mfccs],
            'silence_ratio': float(silence_ratio)
        }
        
        # 임시 파일 삭제
        if os.path.exists(wav_path):
            os.remove(wav_path)
            
        return features
    except Exception as e:
        logger.error(f"Error extracting audio features: {str(e)}")
        return None


def call_callytics(audio_path):
    """
    Callytics (callanalysis 모듈) 호출을 위한 함수
    
    실제 구현에서는 subprocess를 사용하여 별도 프로세스에서 호출하거나
    직접 Python 모듈을 import하여 호출
    """
    try:
        # 방법 1: 모듈 직접 호출 (만약 같은 프로세스에서 실행 가능하다면)
        # import sys
        # sys.path.append(os.path.join(settings.BASE_DIR, '..', 'callanalysis'))
        # from main import process as callytics_process
        # result = callytics_process(audio_path)
        
        # 방법 2: 서브프로세스로 호출
        callanalysis_path = os.path.join(settings.BASE_DIR, '..', 'callanalysis')
        process = subprocess.Popen(
            ['python', 'main.py', audio_path],
            cwd=callanalysis_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            logger.error(f"Error calling Callytics: {stderr.decode('utf-8')}")
            return None
            
        # 결과 파일 읽기 (예시: Callytics가 결과를 JSON으로 출력한다고 가정)
        try:
            result = json.loads(stdout.decode('utf-8'))
        except json.JSONDecodeError:
            # 결과 파일 직접 읽기 (예시 경로)
            result_path = os.path.join(callanalysis_path, '.temp', 'output.json')
            if os.path.exists(result_path):
                with open(result_path, 'r') as f:
                    result = json.load(f)
            else:
                logger.error("No result file found from Callytics")
                return None
                
        return result
    except Exception as e:
        logger.error(f"Error in call_callytics: {str(e)}")
        return None


def format_conversation_for_llm(speakers_data):
    """화자 분리 데이터를 LLM 프롬프트용으로 포맷팅"""
    formatted = ""
    
    # 화자별로 정렬된 발화 목록
    utterances = sorted(speakers_data.get('utterances', []), key=lambda x: x.get('start', 0))
    
    for utterance in utterances:
        speaker = utterance.get('speaker', 'unknown')
        text = utterance.get('text', '')
        
        # 화자 이름 첫글자 대문자로 변경
        speaker_name = speaker.capitalize()
        
        # 포맷팅
        formatted += f"{speaker_name}: {text}\n"
    
    return formatted


def serialize_outputs(call_analysis):
    """프론트엔드 시각화를 위해 분석 결과 직렬화"""
    # 감정 데이터
    emotion_data = call_analysis.emotions or {}
    
    # 토픽 데이터
    topics = call_analysis.key_topics or []
    
    # 만족도 점수
    satisfaction = {
        'score': call_analysis.satisfaction_score,
        'category': call_analysis.satisfaction_category,
        'llm_score': call_analysis.llm_score
    }
    
    # 요약 데이터
    summary = {
        'text': call_analysis.summary,
        'evaluation': call_analysis.llm_evaluation
    }
    
    return {
        'emotions': emotion_data,
        'topics': topics,
        'satisfaction': satisfaction,
        'summary': summary
    } 