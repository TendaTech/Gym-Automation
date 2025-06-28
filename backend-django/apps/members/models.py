import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Member(models.Model):
    MEMBERSHIP_TYPES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
        ('student', 'Student'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    subscription_due_date = models.DateField()
    birthday = models.DateField(null=True, blank=True)
    last_checkin_date = models.DateField(null=True, blank=True)
    emergency_contact = models.TextField(blank=True)
    address = models.TextField(blank=True)
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_TYPES, default='basic')
    notes = models.TextField(blank=True)
    milestones = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    fitness_goals = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_members')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['subscription_due_date']),
            models.Index(fields=['is_active']),
            models.Index(fields=['birthday']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    @property
    def days_until_due(self):
        from datetime import date
        return (self.subscription_due_date - date.today()).days

    @property
    def is_due_soon(self):
        return 0 <= self.days_until_due <= 5

    @property
    def is_overdue(self):
        return self.days_until_due < 0

    @property
    def days_since_checkin(self):
        if not self.last_checkin_date:
            return None
        from datetime import date
        return (date.today() - self.last_checkin_date).days

    @property
    def is_inactive(self):
        return self.days_since_checkin and self.days_since_checkin > 7

    @property
    def is_birthday_today(self):
        if not self.birthday:
            return False
        from datetime import date
        today = date.today()
        return (self.birthday.month == today.month and 
                self.birthday.day == today.day)


class Coach(models.Model):
    SPECIALIZATIONS = [
        ('strength', 'Strength Training'),
        ('cardio', 'Cardio'),
        ('yoga', 'Yoga'),
        ('pilates', 'Pilates'),
        ('crossfit', 'CrossFit'),
        ('boxing', 'Boxing'),
        ('swimming', 'Swimming'),
        ('nutrition', 'Nutrition'),
        ('rehabilitation', 'Rehabilitation'),
        ('general', 'General Fitness'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    specializations = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    certifications = models.JSONField(default=list, blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    profile_image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class WorkoutPlan(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration_weeks = models.PositiveIntegerField()
    sessions_per_week = models.PositiveIntegerField()
    created_by = models.ForeignKey(Coach, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class WorkoutSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='sessions')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    exercises = models.JSONField(default=list)  # List of exercises with sets, reps, etc.
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.workout_plan.name} - {self.name}"


class MemberWorkoutPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='workout_plans')
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    progress_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member.full_name} - {self.workout_plan.name}"


class WorkoutLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='workout_logs')
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    date = models.DateField()
    duration_minutes = models.PositiveIntegerField()
    exercises_completed = models.JSONField(default=list)
    notes = models.TextField(blank=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    calories_burned = models.PositiveIntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['member', 'workout_session', 'date']

    def __str__(self):
        return f"{self.member.full_name} - {self.workout_session.name} - {self.date}"


class CoachSchedule(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    max_clients = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']
        unique_together = ['coach', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.coach.full_name} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class TrainingSession(models.Model):
    SESSION_TYPES = [
        ('personal', 'Personal Training'),
        ('group', 'Group Training'),
        ('class', 'Fitness Class'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='training_sessions')
    members = models.ManyToManyField(Member, related_name='training_sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_participants = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} - {self.date} {self.start_time}"

    @property
    def current_participants(self):
        return self.members.count()

    @property
    def is_full(self):
        return self.current_participants >= self.max_participants


class EmailLog(models.Model):
    EMAIL_TYPES = [
        ('subscription', 'Subscription Reminder'),
        ('inactivity', 'Inactivity Alert'),
        ('birthday', 'Birthday Wish'),
        ('motivational', 'Motivational Email'),
        ('workout_reminder', 'Workout Reminder'),
        ('session_reminder', 'Training Session Reminder'),
    ]

    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='email_logs')
    email_type = models.CharField(max_length=50, choices=EMAIL_TYPES)
    sent_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    email_subject = models.CharField(max_length=255, blank=True)
    email_content = models.TextField(blank=True)

    class Meta:
        ordering = ['-sent_date']
        indexes = [
            models.Index(fields=['member', 'email_type']),
            models.Index(fields=['sent_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.email_type} to {self.member.full_name} - {self.status}"


class MemberCheckin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='checkins')
    checkin_time = models.DateTimeField(auto_now_add=True)
    checkout_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-checkin_time']

    def __str__(self):
        return f"{self.member.full_name} - {self.checkin_time.date()}"

    def save(self, *args, **kwargs):
        if self.checkout_time and self.checkin_time:
            duration = self.checkout_time - self.checkin_time
            self.duration_minutes = int(duration.total_seconds() / 60)
        super().save(*args, **kwargs)