from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import redis
from celery import current_app


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint to verify system status
    """
    health_status = {
        'status': 'healthy',
        'django': 'ok',
        'database': 'ok',
        'redis': 'ok',
        'celery': 'ok'
    }
    
    # Check database
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        health_status['database'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Check Redis
    try:
        r = redis.from_url(settings.CELERY_BROKER_URL)
        r.ping()
    except Exception as e:
        health_status['redis'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Check Celery
    try:
        inspect = current_app.control.inspect()
        stats = inspect.stats()
        if not stats:
            health_status['celery'] = 'no workers available'
        else:
            health_status['celery'] = f'{len(stats)} workers active'
    except Exception as e:
        health_status['celery'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    status_code = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response(health_status, status=status_code)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API root endpoint with available endpoints
    """
    return Response({
        'message': 'Welcome to Gym Automation API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health/',
            'docs': '/api/docs/',
            'auth': '/api/auth/',
            'members': '/api/members/',
        }
    })