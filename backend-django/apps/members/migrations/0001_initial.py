# Generated by Django 4.2.7 on 2025-07-10 19:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('specializations', models.JSONField(blank=True, default=list)),
                ('bio', models.TextField(blank=True)),
                ('experience_years', models.PositiveIntegerField(default=0)),
                ('certifications', models.JSONField(blank=True, default=list)),
                ('hourly_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('profile_image', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('subscription_due_date', models.DateField()),
                ('birthday', models.DateField(blank=True, null=True)),
                ('last_checkin_date', models.DateField(blank=True, null=True)),
                ('emergency_contact', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('membership_type', models.CharField(choices=[('basic', 'Basic'), ('premium', 'Premium'), ('vip', 'VIP'), ('student', 'Student')], default='basic', max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('milestones', models.JSONField(blank=True, default=list)),
                ('is_active', models.BooleanField(default=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('height', models.FloatField(blank=True, help_text='Height in cm', null=True)),
                ('weight', models.FloatField(blank=True, help_text='Weight in kg', null=True)),
                ('fitness_goals', models.TextField(blank=True)),
                ('medical_conditions', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_members', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('difficulty_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=20)),
                ('duration_weeks', models.PositiveIntegerField()),
                ('sessions_per_week', models.PositiveIntegerField()),
                ('is_public', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.coach')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WorkoutSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('duration_minutes', models.PositiveIntegerField()),
                ('exercises', models.JSONField(default=list)),
                ('order', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('workout_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='members.workoutplan')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TrainingSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('session_type', models.CharField(choices=[('personal', 'Personal Training'), ('group', 'Group Training'), ('class', 'Fitness Class')], max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('max_participants', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('no_show', 'No Show')], default='scheduled', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_sessions', to='members.coach')),
                ('members', models.ManyToManyField(related_name='training_sessions', to='members.member')),
            ],
            options={
                'ordering': ['date', 'start_time'],
            },
        ),
        migrations.CreateModel(
            name='MemberWorkoutPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('progress_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('coach', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.coach')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_plans', to='members.member')),
                ('workout_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.workoutplan')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MemberCheckin',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('checkin_time', models.DateTimeField(auto_now_add=True)),
                ('checkout_time', models.DateTimeField(blank=True, null=True)),
                ('duration_minutes', models.PositiveIntegerField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkins', to='members.member')),
            ],
            options={
                'ordering': ['-checkin_time'],
            },
        ),
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email_type', models.CharField(choices=[('subscription', 'Subscription Reminder'), ('inactivity', 'Inactivity Alert'), ('birthday', 'Birthday Wish'), ('motivational', 'Motivational Email'), ('workout_reminder', 'Workout Reminder'), ('session_reminder', 'Training Session Reminder')], max_length=50)),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending', max_length=20)),
                ('error_message', models.TextField(blank=True)),
                ('email_subject', models.CharField(blank=True, max_length=255)),
                ('email_content', models.TextField(blank=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_logs', to='members.member')),
            ],
            options={
                'ordering': ['-sent_date'],
            },
        ),
        migrations.CreateModel(
            name='CoachSchedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('day_of_week', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('max_clients', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='members.coach')),
            ],
            options={
                'ordering': ['day_of_week', 'start_time'],
            },
        ),
        migrations.CreateModel(
            name='WorkoutLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('duration_minutes', models.PositiveIntegerField()),
                ('exercises_completed', models.JSONField(default=list)),
                ('notes', models.TextField(blank=True)),
                ('rating', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('calories_burned', models.PositiveIntegerField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_logs', to='members.member')),
                ('workout_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.workoutsession')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('member', 'workout_session', 'date')},
            },
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['email'], name='members_mem_email_afed21_idx'),
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['subscription_due_date'], name='members_mem_subscri_456329_idx'),
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['is_active'], name='members_mem_is_acti_65d5c9_idx'),
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['birthday'], name='members_mem_birthda_5ad43f_idx'),
        ),
        migrations.AddIndex(
            model_name='emaillog',
            index=models.Index(fields=['member', 'email_type'], name='members_ema_member__71d128_idx'),
        ),
        migrations.AddIndex(
            model_name='emaillog',
            index=models.Index(fields=['sent_date'], name='members_ema_sent_da_d34d04_idx'),
        ),
        migrations.AddIndex(
            model_name='emaillog',
            index=models.Index(fields=['status'], name='members_ema_status_901db0_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='coachschedule',
            unique_together={('coach', 'day_of_week', 'start_time')},
        ),
    ]
