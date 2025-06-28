from django.contrib import admin
from .models import (
    Member, Coach, WorkoutPlan, WorkoutSession, MemberWorkoutPlan,
    WorkoutLog, CoachSchedule, TrainingSession, EmailLog, MemberCheckin
)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'membership_type', 'subscription_due_date',
        'is_active', 'last_checkin_date', 'created_at'
    ]
    list_filter = [
        'is_active', 'membership_type', 'subscription_due_date', 'created_at', 'gender'
    ]
    search_fields = ['full_name', 'email', 'phone']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'email', 'phone', 'is_active', 'user')
        }),
        ('Membership Details', {
            'fields': ('membership_type', 'subscription_due_date', 'last_checkin_date')
        }),
        ('Personal Information', {
            'fields': ('birthday', 'gender', 'height', 'weight', 'address', 'emergency_contact')
        }),
        ('Health & Fitness', {
            'fields': ('fitness_goals', 'medical_conditions', 'milestones', 'notes')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by', 'user')


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'experience_years', 'is_available', 'created_at'
    ]
    list_filter = ['is_available', 'experience_years', 'specializations']
    search_fields = ['full_name', 'email', 'specializations']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'difficulty_level', 'duration_weeks', 'sessions_per_week',
        'created_by', 'is_public', 'created_at'
    ]
    list_filter = ['difficulty_level', 'is_public', 'created_by']
    search_fields = ['name', 'description']


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'workout_plan', 'duration_minutes', 'order']
    list_filter = ['workout_plan']
    search_fields = ['name', 'description']


@admin.register(MemberWorkoutPlan)
class MemberWorkoutPlanAdmin(admin.ModelAdmin):
    list_display = [
        'member', 'workout_plan', 'coach', 'start_date', 'end_date', 'is_active'
    ]
    list_filter = ['is_active', 'coach', 'start_date']
    search_fields = ['member__full_name', 'workout_plan__name']


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = [
        'member', 'workout_session', 'date', 'duration_minutes', 'completed', 'rating'
    ]
    list_filter = ['completed', 'date', 'rating']
    search_fields = ['member__full_name', 'workout_session__name']


@admin.register(CoachSchedule)
class CoachScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'coach', 'get_day_of_week_display', 'start_time', 'end_time',
        'is_available', 'max_clients'
    ]
    list_filter = ['day_of_week', 'is_available', 'coach']


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'coach', 'session_type', 'date', 'start_time',
        'current_participants', 'max_participants', 'status'
    ]
    list_filter = ['session_type', 'status', 'date', 'coach']
    search_fields = ['title', 'description']
    filter_horizontal = ['members']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = [
        'member', 'email_type', 'status', 'sent_date', 'email_subject'
    ]
    list_filter = ['email_type', 'status', 'sent_date']
    search_fields = ['member__full_name', 'member__email', 'email_subject']
    readonly_fields = ['id', 'sent_date']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('member')


@admin.register(MemberCheckin)
class MemberCheckinAdmin(admin.ModelAdmin):
    list_display = [
        'member', 'checkin_time', 'checkout_time', 'duration_minutes'
    ]
    list_filter = ['checkin_time']
    search_fields = ['member__full_name']
    readonly_fields = ['duration_minutes']