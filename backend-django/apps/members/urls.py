from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'members', views.MemberViewSet)
router.register(r'coaches', views.CoachViewSet)
router.register(r'workout-plans', views.WorkoutPlanViewSet)
router.register(r'workout-logs', views.WorkoutLogViewSet)
router.register(r'training-sessions', views.TrainingSessionViewSet)
router.register(r'checkins', views.MemberCheckinViewSet)

urlpatterns = [
    # API Routes
    path('api/', include(router.urls)),
    
    # Email management
    path('emails/logs/', views.EmailLogListView.as_view(), name='email-log-list'),

    path('api/emails/send/', views.SendEmailView.as_view(), name='send-email'),
    path('api/emails/send-reminders/', views.send_subscription_reminders_view, name='send-reminders'),
    path('api/emails/send-motivational/', views.send_motivational_emails_view, name='send-motivational'),
    
    # Member Portal

    # implement Checkings endpoint 
    path('portal/dashboard/', views.MemberPortalDashboardView.as_view(), name='member-portal-dashboard'),

    path('api/coaches/available/', views.available_coaches, name='available-coaches'), 
    
    # Legacy URLs for backward compatibility
    path('', views.MemberViewSet.as_view({'get': 'list', 'post': 'create'}), name='member-list-create'),
    path('<uuid:pk>/', views.MemberViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='member-detail'),
    path('stats/', views.MemberViewSet.as_view({'get': 'stats'}), name='member-stats'),
]