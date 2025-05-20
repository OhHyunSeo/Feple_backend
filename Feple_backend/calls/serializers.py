from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Agent, CallRawData, CallTranscript, 
    CallAnalysis, AgentCoaching, ProcessingTask
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'username']


class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Agent
        fields = ['id', 'user', 'employee_id', 'department', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CallRawDataSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source='agent.user.get_full_name', read_only=True)
    
    class Meta:
        model = CallRawData
        fields = [
            'id', 'audio_file', 'agent', 'agent_name', 'call_date', 
            'duration', 'caller_number', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class CallTranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallTranscript
        fields = [
            'id', 'call', 'full_transcript', 'speakers_json',
            'silence_rate', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CallAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallAnalysis
        fields = [
            'id', 'call', 'satisfaction_score', 'satisfaction_category',
            'llm_evaluation', 'llm_score', 'key_topics', 'emotions',
            'summary', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AgentCoachingSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source='agent.user.get_full_name', read_only=True)
    
    class Meta:
        model = AgentCoaching
        fields = [
            'id', 'agent', 'agent_name', 'date', 'daily_summary',
            'coaching_points', 'strengths', 'areas_to_improve',
            'call_count', 'avg_satisfaction', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProcessingTaskSerializer(serializers.ModelSerializer):
    task_type_display = serializers.CharField(source='get_task_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ProcessingTask
        fields = [
            'id', 'call', 'agent', 'task_type', 'task_type_display',
            'status', 'status_display', 'task_id', 'error_message',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'task_id', 'created_at', 'updated_at']


class CallDetailSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)
    transcript = CallTranscriptSerializer(read_only=True)
    analysis = CallAnalysisSerializer(read_only=True)
    tasks = ProcessingTaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = CallRawData
        fields = [
            'id', 'audio_file', 'agent', 'call_date', 'duration',
            'caller_number', 'status', 'transcript', 'analysis',
            'tasks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 