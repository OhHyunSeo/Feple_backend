from django.contrib import admin
from .models import (
    Agent, CallRawData, CallTranscript, 
    CallAnalysis, AgentCoaching, ProcessingTask
)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_id', 'get_full_name', 'department', 'created_at')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__email')
    list_filter = ('department', 'created_at')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = '이름'


@admin.register(CallRawData)
class CallRawDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'call_date', 'duration', 'status', 'created_at')
    list_filter = ('status', 'call_date', 'created_at')
    search_fields = ('agent__user__first_name', 'agent__user__last_name', 'caller_number')
    date_hierarchy = 'call_date'


@admin.register(CallTranscript)
class CallTranscriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'call', 'silence_rate', 'created_at')
    search_fields = ('call__id', 'full_transcript')
    list_filter = ('created_at',)


@admin.register(CallAnalysis)
class CallAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'call', 'satisfaction_score', 'satisfaction_category', 'llm_score')
    list_filter = ('satisfaction_category', 'created_at')
    search_fields = ('call__id', 'summary', 'llm_evaluation')


@admin.register(AgentCoaching)
class AgentCoachingAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'date', 'call_count', 'avg_satisfaction')
    list_filter = ('date',)
    search_fields = ('agent__user__first_name', 'agent__user__last_name', 'daily_summary')
    date_hierarchy = 'date'


@admin.register(ProcessingTask)
class ProcessingTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_type', 'status', 'get_entity', 'created_at')
    list_filter = ('task_type', 'status', 'created_at')
    search_fields = ('call__id', 'agent__employee_id', 'error_message')
    
    def get_entity(self, obj):
        if obj.call:
            return f"Call {obj.call.id}"
        elif obj.agent:
            return f"Agent {obj.agent.employee_id}"
        else:
            return "N/A"
    get_entity.short_description = '관련 항목'
