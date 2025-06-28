import pandas as pd
from datetime import date, timedelta
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Member, Coach, WorkoutPlan, WorkoutSession, MemberWorkoutPlan,
    WorkoutLog, CoachSchedule, TrainingSession, EmailLog, MemberCheckin
)
from .serializers import (
    MemberSerializer, CoachSerializer, WorkoutPlanSerializer, WorkoutSessionSerializer,
    MemberWorkoutPlanSerializer, WorkoutLogSerializer, CoachScheduleSerializer,
    TrainingSessionSerializer, EmailLogSerializer, MemberCheckinSerializer,
    MemberStatsSerializer, MemberDashboardSerializer, BulkMemberUploadSerializer,
    EmailSendSerializer
)
from .filters import MemberFilter
from .tasks import (
    send_subscription_reminders, send_motivational_emails,
    send_birthday_wishes, send_inactivity_alerts
)


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MemberFilter
    search_fields = ['full_name', 'email', 'phone']
    ordering_fields = ['full_name', 'subscription_due_date', 'created_at', 'last_checkin_date']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        today = date.today()
        month_start = today.replace(day=1)
        
        total_members = Member.objects.count()
        active_members = Member.objects.filter(is_active=True).count()
        inactive_members = total_members - active_members
        
        due_soon_date = today + timedelta(days=5)
        due_soon = Member.objects.filter(
            subscription_due_date__gte=today,
            subscription_due_date__lte=due_soon_date,
            is_active=True
        ).count()
        
        overdue = Member.objects.filter(
            subscription_due_date__lt=today,
            is_active=True
        ).count()
        
        birthdays_today = Member.objects.filter(
            birthday__month=today.month,
            birthday__day=today.day,
            is_active=True
        ).count()
        
        new_this_month = Member.objects.filter(
            created_at__gte=month_start
        ).count()
        
        membership_types = dict(
            Member.objects.values_list('membership_type').annotate(
                count=Count('membership_type')
            )
        )
        
        stats = {
            'total_members': total_members,
            'active_members': active_members,
            'inactive_members': inactive_members,
            'due_soon': due_soon,
            'overdue': overdue,
            'birthdays_today': birthdays_today,
            'new_this_month': new_this_month,
            'membership_types': membership_types,
        }
        
        serializer = MemberStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        member = self.get_object()
        
        # Get current workout plan
        current_plan = MemberWorkoutPlan.objects.filter(
            member=member, is_active=True
        ).first()
        
        # Get recent workouts (last 10)
        recent_workouts = WorkoutLog.objects.filter(
            member=member
        ).order_by('-date')[:10]
        
        # Get upcoming training sessions
        upcoming_sessions = TrainingSession.objects.filter(
            members=member,
            date__gte=date.today(),
            status='scheduled'
        ).order_by('date', 'start_time')[:5]
        
        # Calculate workout streak
        workout_streak = self._calculate_workout_streak(member)
        
        # Total workouts
        total_workouts = WorkoutLog.objects.filter(member=member, completed=True).count()
        
        # Missed workouts (scheduled but not completed)
        missed_workouts = WorkoutLog.objects.filter(member=member, completed=False).count()
        
        dashboard_data = {
            'member': member,
            'current_workout_plan': current_plan,
            'recent_workouts': recent_workouts,
            'upcoming_sessions': upcoming_sessions,
            'workout_streak': workout_streak,
            'total_workouts': total_workouts,
            'missed_workouts': missed_workouts,
        }
        
        serializer = MemberDashboardSerializer(dashboard_data)
        return Response(serializer.data)

    def _calculate_workout_streak(self, member):
        # Calculate consecutive days with workouts
        today = date.today()
        streak = 0
        current_date = today
        
        while True:
            if WorkoutLog.objects.filter(
                member=member, 
                date=current_date, 
                completed=True
            ).exists():
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
                
        return streak

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def bulk_upload(self, request):
        serializer = BulkMemberUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file = serializer.validated_data['file']
        
        try:
            # Read the file
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            created_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Map CSV columns to model fields
                    member_data = {
                        'full_name': row.get('full_name', ''),
                        'email': row.get('email', ''),
                        'phone': row.get('phone', ''),
                        'subscription_due_date': pd.to_datetime(row.get('subscription_due_date')).date(),
                        'membership_type': row.get('membership_type', 'basic'),
                        'is_active': row.get('is_active', True),
                    }
                    
                    # Optional fields
                    if pd.notna(row.get('birthday')):
                        member_data['birthday'] = pd.to_datetime(row.get('birthday')).date()
                    
                    if pd.notna(row.get('last_checkin_date')):
                        member_data['last_checkin_date'] = pd.to_datetime(row.get('last_checkin_date')).date()
                    
                    # Create member
                    member_serializer = MemberSerializer(data=member_data)
                    if member_serializer.is_valid():
                        member_serializer.save(created_by=request.user)
                        created_count += 1
                    else:
                        errors.append(f"Row {index + 1}: {member_serializer.errors}")
                        
                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
            
            return Response({
                'message': f'Successfully created {created_count} members',
                'errors': errors
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': f'Failed to process file: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class CoachViewSet(ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'specializations']
    ordering_fields = ['full_name', 'experience_years', 'created_at']
    ordering = ['full_name']

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        coach = self.get_object()
        schedules = CoachSchedule.objects.filter(coach=coach)
        serializer = CoachScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        coach = self.get_object()
        date_param = request.query_params.get('date', date.today())
        
        if isinstance(date_param, str):
            date_param = pd.to_datetime(date_param).date()
        
        day_of_week = date_param.weekday()
        
        # Get coach's schedule for the day
        schedules = CoachSchedule.objects.filter(
            coach=coach,
            day_of_week=day_of_week,
            is_available=True
        )
        
        # Get existing sessions for the day
        existing_sessions = TrainingSession.objects.filter(
            coach=coach,
            date=date_param,
            status__in=['scheduled', 'completed']
        )
        
        availability = []
        for schedule in schedules:
            # Check if time slot is available
            conflicting_sessions = existing_sessions.filter(
                start_time__lt=schedule.end_time,
                end_time__gt=schedule.start_time
            )
            
            available_slots = schedule.max_clients - conflicting_sessions.count()
            
            availability.append({
                'schedule_id': schedule.id,
                'start_time': schedule.start_time,
                'end_time': schedule.end_time,
                'available_slots': max(0, available_slots),
                'max_clients': schedule.max_clients
            })
        
        return Response(availability)


class WorkoutPlanViewSet(ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'difficulty_level', 'created_at']
    filterset_fields = ['difficulty_level', 'created_by', 'is_public']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # Assuming the user is a coach
        coach = Coach.objects.get(user=self.request.user)
        serializer.save(created_by=coach)


class WorkoutLogViewSet(ModelViewSet):
    queryset = WorkoutLog.objects.all()
    serializer_class = WorkoutLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['member', 'workout_session', 'date', 'completed']
    ordering = ['-date']

    def get_queryset(self):
        # If user is a member, only show their logs
        if hasattr(self.request.user, 'member'):
            return WorkoutLog.objects.filter(member=self.request.user.member)
        return WorkoutLog.objects.all()


class TrainingSessionViewSet(ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['coach', 'session_type', 'date', 'status']
    ordering = ['date', 'start_time']

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        session = self.get_object()
        member = Member.objects.get(user=request.user)
        
        if session.is_full:
            return Response(
                {'error': 'Session is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session.members.add(member)
        return Response({'message': 'Successfully joined session'})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        session = self.get_object()
        member = Member.objects.get(user=request.user)
        
        session.members.remove(member)
        return Response({'message': 'Successfully left session'})


class MemberCheckinViewSet(ModelViewSet):
    queryset = MemberCheckin.objects.all()
    serializer_class = MemberCheckinSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['member']
    ordering = ['-checkin_time']

    def get_queryset(self):
        # If user is a member, only show their checkins
        if hasattr(self.request.user, 'member'):
            return MemberCheckin.objects.filter(member=self.request.user.member)
        return MemberCheckin.objects.all()

    @action(detail=False, methods=['post'])
    def checkin(self, request):
        member = Member.objects.get(user=request.user)
        
        # Check if already checked in today
        today = timezone.now().date()
        existing_checkin = MemberCheckin.objects.filter(
            member=member,
            checkin_time__date=today,
            checkout_time__isnull=True
        ).first()
        
        if existing_checkin:
            return Response(
                {'error': 'Already checked in today'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        checkin = MemberCheckin.objects.create(member=member)
        
        # Update member's last checkin date
        member.last_checkin_date = today
        member.save()
        
        serializer = MemberCheckinSerializer(checkin)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        member = Member.objects.get(user=request.user)
        
        # Find today's checkin
        today = timezone.now().date()
        checkin = MemberCheckin.objects.filter(
            member=member,
            checkin_time__date=today,
            checkout_time__isnull=True
        ).first()
        
        if not checkin:
            return Response(
                {'error': 'No active checkin found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        checkin.checkout_time = timezone.now()
        checkin.save()
        
        serializer = MemberCheckinSerializer(checkin)
        return Response(serializer.data)


class EmailLogListView(generics.ListAPIView):
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['email_type', 'status', 'member']
    ordering = ['-sent_date']


class SendEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EmailSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email_type = serializer.validated_data['email_type']
        member_ids = serializer.validated_data.get('member_ids')
        force_send = serializer.validated_data.get('force_send', False)
        
        task_map = {
            'subscription': send_subscription_reminders,
            'motivational': send_motivational_emails,
            'birthday': send_birthday_wishes,
            'inactivity': send_inactivity_alerts,
        }
        
        task = task_map.get(email_type)
        if not task:
            return Response(
                {'error': 'Invalid email type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task_result = task.delay(member_ids=member_ids, force_send=force_send)
        
        return Response({
            'message': f'{email_type.title()} emails are being sent',
            'task_id': task_result.id
        }, status=status.HTTP_202_ACCEPTED)


# Member Portal Views (for members to access their own data)
class MemberPortalDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            member = Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            return Response(
                {'error': 'Member profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get current workout plan
        current_plan = MemberWorkoutPlan.objects.filter(
            member=member, is_active=True
        ).first()
        
        # Get recent workouts
        recent_workouts = WorkoutLog.objects.filter(
            member=member
        ).order_by('-date')[:10]
        
        # Get upcoming sessions
        upcoming_sessions = TrainingSession.objects.filter(
            members=member,
            date__gte=date.today(),
            status='scheduled'
        ).order_by('date', 'start_time')[:5]
        
        # Calculate stats
        total_workouts = WorkoutLog.objects.filter(member=member, completed=True).count()
        this_month_workouts = WorkoutLog.objects.filter(
            member=member,
            completed=True,
            date__month=date.today().month,
            date__year=date.today().year
        ).count()
        
        # Calculate workout streak
        streak = 0
        current_date = date.today()
        while WorkoutLog.objects.filter(
            member=member, 
            date=current_date, 
            completed=True
        ).exists():
            streak += 1
            current_date -= timedelta(days=1)
        
        dashboard_data = {
            'member': MemberSerializer(member).data,
            'current_workout_plan': MemberWorkoutPlanSerializer(current_plan).data if current_plan else None,
            'recent_workouts': WorkoutLogSerializer(recent_workouts, many=True).data,
            'upcoming_sessions': TrainingSessionSerializer(upcoming_sessions, many=True).data,
            'stats': {
                'total_workouts': total_workouts,
                'this_month_workouts': this_month_workouts,
                'workout_streak': streak,
                'membership_status': 'Active' if member.is_active else 'Inactive',
                'days_until_due': member.days_until_due
            }
        }
        
        return Response(dashboard_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_coaches(request):
    """Get available coaches for a specific date and time"""
    date_param = request.query_params.get('date', date.today())
    
    if isinstance(date_param, str):
        date_param = pd.to_datetime(date_param).date()
    
    day_of_week = date_param.weekday()
    
    # Get coaches available on this day
    available_coaches = Coach.objects.filter(
        is_available=True,
        schedules__day_of_week=day_of_week,
        schedules__is_available=True
    ).distinct()
    
    serializer = CoachSerializer(available_coaches, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_subscription_reminders_view(request):
    task_result = send_subscription_reminders.delay()
    return Response({
        'message': 'Subscription reminders are being sent',
        'task_id': task_result.id
    }, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_motivational_emails_view(request):
    task_result = send_motivational_emails.delay()
    return Response({
        'message': 'Motivational emails are being sent',
        'task_id': task_result.id
    }, status=status.HTTP_202_ACCEPTED)