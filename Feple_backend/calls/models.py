from django.db import models
from django.contrib.auth.models import User


class Agent(models.Model):
    """상담원 모델"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent')
    employee_id = models.CharField("직원 ID", max_length=20, unique=True)
    department = models.CharField("부서", max_length=50, blank=True)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "상담원"
        verbose_name_plural = "상담원들"
        
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


class CallRawData(models.Model):
    """원본 통화 데이터 모델"""
    STATUS_CHOICES = (
        ('pending', '처리 대기'),
        ('processing', '처리 중'),
        ('completed', '처리 완료'),
        ('failed', '처리 실패'),
    )
    
    audio_file = models.FileField("오디오 파일", upload_to='audio/')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='calls')
    call_date = models.DateTimeField("통화 일시")
    duration = models.IntegerField("통화 시간(초)", null=True, blank=True)
    caller_number = models.CharField("발신자 번호", max_length=20, blank=True)
    status = models.CharField("처리 상태", max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "원본 통화 데이터"
        verbose_name_plural = "원본 통화 데이터들"
        ordering = ['-call_date']
        
    def __str__(self):
        return f"Call {self.id} - {self.agent.user.get_full_name()} ({self.call_date.strftime('%Y-%m-%d %H:%M')})"


class CallTranscript(models.Model):
    """통화 전사 데이터 모델"""
    call = models.OneToOneField(CallRawData, on_delete=models.CASCADE, related_name='transcript')
    full_transcript = models.TextField("전체 전사 내용")
    speakers_json = models.JSONField("화자 분리 데이터", default=dict)
    silence_rate = models.FloatField("침묵률(%)", null=True, blank=True)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "통화 전사 데이터"
        verbose_name_plural = "통화 전사 데이터들"
    
    def __str__(self):
        return f"Transcript for Call {self.call.id}"


class CallAnalysis(models.Model):
    """통화 분석 결과 모델"""
    call = models.OneToOneField(CallRawData, on_delete=models.CASCADE, related_name='analysis')
    satisfaction_score = models.FloatField("만족도 점수", null=True, blank=True)
    satisfaction_category = models.CharField("만족도 카테고리", max_length=20, blank=True)
    llm_evaluation = models.TextField("LLM 평가 내용", blank=True)
    llm_score = models.FloatField("LLM 평가 점수", null=True, blank=True)
    key_topics = models.JSONField("주요 토픽", blank=True, null=True)
    emotions = models.JSONField("감정 분석", blank=True, null=True)
    summary = models.TextField("요약", blank=True)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "통화 분석 결과"
        verbose_name_plural = "통화 분석 결과들"
    
    def __str__(self):
        return f"Analysis for Call {self.call.id}"


class AgentCoaching(models.Model):
    """상담원 코칭 모델"""
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='coaching')
    date = models.DateField("날짜")
    daily_summary = models.TextField("하루 요약")
    coaching_points = models.TextField("코칭 포인트")
    strengths = models.TextField("강점", blank=True)
    areas_to_improve = models.TextField("개선 영역", blank=True)
    call_count = models.IntegerField("통화 수", default=0)
    avg_satisfaction = models.FloatField("평균 만족도", null=True, blank=True)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "상담원 코칭"
        verbose_name_plural = "상담원 코칭들"
        unique_together = ('agent', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"Coaching for {self.agent.user.get_full_name()} on {self.date}"


class ProcessingTask(models.Model):
    """비동기 작업 모니터링 모델"""
    TASK_TYPES = (
        ('transcription', '음성 전사'),
        ('analysis', '통화 분석'),
        ('llm_evaluation', 'LLM 평가'),
        ('coaching', '코칭 생성'),
    )
    
    STATUS_CHOICES = (
        ('pending', '대기 중'),
        ('processing', '처리 중'),
        ('completed', '완료'),
        ('failed', '실패'),
    )
    
    call = models.ForeignKey(CallRawData, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    task_type = models.CharField("작업 유형", max_length=20, choices=TASK_TYPES)
    status = models.CharField("상태", max_length=20, choices=STATUS_CHOICES, default='pending')
    task_id = models.CharField("Celery 작업 ID", max_length=50, blank=True)
    error_message = models.TextField("오류 메시지", blank=True)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "처리 작업"
        verbose_name_plural = "처리 작업들"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_task_type_display()} for {'Call ' + str(self.call.id) if self.call else 'Agent ' + str(self.agent.id)}"
