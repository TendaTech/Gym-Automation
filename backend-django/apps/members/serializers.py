from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Member, Coach, WorkoutPlan, WorkoutSession, MemberWorkoutPlan,
    WorkoutLog, CoachSchedule, TrainingSession, EmailLog, MemberCheckin
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class MemberSerializer(serializers.ModelSerializer):
    days_until_due = serializers.ReadOnlyField()
    is_due_soon = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    days_since_checkin = serializers.ReadOnlyField()
    is_inactive = serializers.ReadOnlyField()
    is_birthday_today = serializers.ReadOnlyField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Member
        fields = [
            'id', 'user', 'full_name', 'email', 'phone', 'subscription_due_date',
            'birthday', 'last_checkin_date', 'emergency_contact', 'address',
            'membership_type', 'notes', 'milestones', 'is_active', 'gender',
            'height', 'weight', 'fitness_goals', 'medical_conditions',
            'created_at', 'updated_at', 'days_until_due', 'is_due_soon',
            'is_overdue', 'days_since_checkin', 'is_inactive', 'is_birthday_today'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        instance = getattr(self, 'instance', None)
        if Member.objects.exclude(pk=instance.pk if instance else None).filter(email=value).exists():
            raise serializers.ValidationError("A member with this email already exists.")
        return value


class CoachSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Coach
        fields = [
            'id', 'user', 'full_name', 'email', 'phone', 'specializations',
            'bio', 'experience_years', 'certifications', 'hourly_rate',
            'is_available', 'profile_image', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = [
            'id', 'name', 'description', 'duration_minutes', 'exercises', 'order'
        ]


class WorkoutPlanSerializer(serializers.ModelSerializer):
    sessions = WorkoutSessionSerializer(many=True, read_only=True)
    created_by = CoachSerializer(read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = [
            'id', 'name', 'description', 'difficulty_level', 'duration_weeks',
            'sessions_per_week', 'created_by', 'is_public', 'sessions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MemberWorkoutPlanSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    workout_plan = WorkoutPlanSerializer(read_only=True)
    coach = CoachSerializer(read_only=True)

    class Meta:
        model = MemberWorkoutPlan
        fields = [
            'id', 'member', 'workout_plan', 'coach', 'start_date', 'end_date',
            'is_active', 'progress_notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class WorkoutLogSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    workout_session = WorkoutSessionSerializer(read_only=True)

    class Meta:
        model = WorkoutLog
        fields = [
            'id', 'member', 'workout_session', 'date', 'duration_minutes',
            'exercises_completed', 'notes', 'rating', 'calories_burned',
            'completed', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CoachScheduleSerializer(serializers.ModelSerializer):
    coach = CoachSerializer(read_only=True)
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = CoachSchedule
        fields = [
            'id', 'coach', 'day_of_week', 'day_name', 'start_time', 'end_time',
            'is_available', 'max_clients', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TrainingSessionSerializer(serializers.ModelSerializer):
    coach = CoachSerializer(read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    current_participants = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()

    class Meta:
        model = TrainingSession
        fields = [
            'id', 'coach', 'members', 'session_type', 'title', 'description',
            'date', 'start_time', 'end_time', 'max_participants', 'status',
            'notes', 'current_participants', 'is_full', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmailLogSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    member_email = serializers.CharField(source='member.email', read_only=True)

    class Meta:
        model = EmailLog
        fields = [
            'id', 'member', 'member_name', 'member_email', 'email_type',
            'sent_date', 'status', 'error_message', 'email_subject'
        ]
        read_only_fields = ['id', 'sent_date']


class MemberCheckinSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)

    class Meta:
        model = MemberCheckin
        fields = [
            'id', 'member', 'checkin_time', 'checkout_time', 'duration_minutes', 'notes'
        ]
        read_only_fields = ['id', 'checkin_time', 'duration_minutes']


class MemberStatsSerializer(serializers.Serializer):
    total_members = serializers.IntegerField()
    active_members = serializers.IntegerField()
    inactive_members = serializers.IntegerField()
    due_soon = serializers.IntegerField()
    overdue = serializers.IntegerField()
    birthdays_today = serializers.IntegerField()
    new_this_month = serializers.IntegerField()
    membership_types = serializers.DictField()


class MemberDashboardSerializer(serializers.Serializer):
    member = MemberSerializer()
    current_workout_plan = MemberWorkoutPlanSerializer()
    recent_workouts = WorkoutLogSerializer(many=True)
    upcoming_sessions = TrainingSessionSerializer(many=True)
    workout_streak = serializers.IntegerField()
    total_workouts = serializers.IntegerField()
    missed_workouts = serializers.IntegerField()


class BulkMemberUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(('.xlsx', '.xls', '.csv')):
            raise serializers.ValidationError("File must be Excel (.xlsx, .xls) or CSV format")
        return value


class EmailSendSerializer(serializers.Serializer):
    email_type = serializers.ChoiceField(choices=EmailLog.EMAIL_TYPES)
    member_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        help_text="List of member IDs. If not provided, will send to all eligible members."
    )
    force_send = serializers.BooleanField(
        default=False,
        help_text="Force send even if recently sent to the same member"
    )