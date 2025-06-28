from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date, timedelta
from .models import Member, EmailLog
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_subscription_reminders(member_ids=None, force_send=False):
    """
    Send subscription reminder emails to members whose subscriptions are due soon
    """
    today = date.today()
    due_soon_date = today + timedelta(days=5)
    
    # Get members with subscriptions due in the next 5 days
    queryset = Member.objects.filter(
        subscription_due_date__gte=today,
        subscription_due_date__lte=due_soon_date,
        is_active=True
    )
    
    if member_ids:
        queryset = queryset.filter(id__in=member_ids)
    
    sent_count = 0
    failed_count = 0
    
    for member in queryset:
        # Check if we've already sent a reminder recently (unless force_send)
        if not force_send:
            recent_log = EmailLog.objects.filter(
                member=member,
                email_type='subscription',
                status='sent',
                sent_date__gte=today - timedelta(days=1)
            ).exists()
            
            if recent_log:
                logger.info(f"Skipping {member.email} - reminder already sent recently")
                continue
        
        try:
            # Prepare email content
            context = {
                'member': member,
                'days_until_due': member.days_until_due,
                'frontend_url': settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:5173',
            }
            
            subject = f"Subscription Reminder - Due in {member.days_until_due} days"
            html_content = render_to_string('emails/subscription_reminder.html', context)
            text_content = render_to_string('emails/subscription_reminder.txt', context)
            
            # Send email
            send_mail(
                subject=subject,
                message=text_content,
                from_email=f"{settings.DEFAULT_FROM_NAME} <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[member.email],
                html_message=html_content,
                fail_silently=False,
            )
            
            # Log successful send
            EmailLog.objects.create(
                member=member,
                email_type='subscription',
                status='sent',
                email_subject=subject,
                email_content=html_content
            )
            
            sent_count += 1
            logger.info(f"Subscription reminder sent to {member.email}")
            
        except Exception as e:
            # Log failed send
            EmailLog.objects.create(
                member=member,
                email_type='subscription',
                status='failed',
                error_message=str(e),
                email_subject=subject if 'subject' in locals() else 'Subscription Reminder'
            )
            
            failed_count += 1
            logger.error(f"Failed to send subscription reminder to {member.email}: {str(e)}")
    
    logger.info(f"Subscription reminders completed: {sent_count} sent, {failed_count} failed")
    return {'sent': sent_count, 'failed': failed_count}


@shared_task
def send_motivational_emails(member_ids=None, force_send=False):
    """
    Send motivational emails to active members
    """
    today = date.today()
    
    # Get active members
    queryset = Member.objects.filter(is_active=True)
    
    if member_ids:
        queryset = queryset.filter(id__in=member_ids)
    
    sent_count = 0
    failed_count = 0
    
    for member in queryset:
        # Check if we've already sent a motivational email recently (unless force_send)
        if not force_send:
            recent_log = EmailLog.objects.filter(
                member=member,
                email_type='motivational',
                status='sent',
                sent_date__gte=today - timedelta(days=7)  # Once per week
            ).exists()
            
            if recent_log:
                logger.info(f"Skipping {member.email} - motivational email already sent recently")
                continue
        
        try:
            # Prepare email content
            context = {
                'member': member,
                'frontend_url': settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:5173',
            }
            
            subject = "Stay Strong! Your Fitness Journey Continues"
            html_content = render_to_string('emails/motivational_email.html', context)
            text_content = render_to_string('emails/motivational_email.txt', context)
            
            # Send email
            send_mail(
                subject=subject,
                message=text_content,
                from_email=f"{settings.DEFAULT_FROM_NAME} <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[member.email],
                html_message=html_content,
                fail_silently=False,
            )
            
            # Log successful send
            EmailLog.objects.create(
                member=member,
                email_type='motivational',
                status='sent',
                email_subject=subject,
                email_content=html_content
            )
            
            sent_count += 1
            logger.info(f"Motivational email sent to {member.email}")
            
        except Exception as e:
            # Log failed send
            EmailLog.objects.create(
                member=member,
                email_type='motivational',
                status='failed',
                error_message=str(e),
                email_subject=subject if 'subject' in locals() else 'Motivational Email'
            )
            
            failed_count += 1
            logger.error(f"Failed to send motivational email to {member.email}: {str(e)}")
    
    logger.info(f"Motivational emails completed: {sent_count} sent, {failed_count} failed")
    return {'sent': sent_count, 'failed': failed_count}


@shared_task
def send_birthday_wishes(member_ids=None, force_send=False):
    """
    Send birthday wishes to members whose birthday is today
    """
    today = date.today()
    
    # Get members with birthday today
    queryset = Member.objects.filter(
        birthday__month=today.month,
        birthday__day=today.day,
        is_active=True
    )
    
    if member_ids:
        queryset = queryset.filter(id__in=member_ids)
    
    sent_count = 0
    failed_count = 0
    
    for member in queryset:
        # Check if we've already sent a birthday wish today (unless force_send)
        if not force_send:
            recent_log = EmailLog.objects.filter(
                member=member,
                email_type='birthday',
                status='sent',
                sent_date__date=today
            ).exists()
            
            if recent_log:
                logger.info(f"Skipping {member.email} - birthday wish already sent today")
                continue
        
        try:
            # Calculate age if birth year is available
            age = None
            if member.birthday and member.birthday.year > 1900:
                age = today.year - member.birthday.year
            
            # Prepare email content
            context = {
                'member': member,
                'age': age,
                'frontend_url': settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:5173',
            }
            
            subject = f"Happy Birthday, {member.full_name.split()[0]}! 🎉"
            html_content = render_to_string('emails/birthday_wish.html', context)
            text_content = render_to_string('emails/birthday_wish.txt', context)
            
            # Send email
            send_mail(
                subject=subject,
                message=text_content,
                from_email=f"{settings.DEFAULT_FROM_NAME} <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[member.email],
                html_message=html_content,
                fail_silently=False,
            )
            
            # Log successful send
            EmailLog.objects.create(
                member=member,
                email_type='birthday',
                status='sent',
                email_subject=subject,
                email_content=html_content
            )
            
            sent_count += 1
            logger.info(f"Birthday wish sent to {member.email}")
            
        except Exception as e:
            # Log failed send
            EmailLog.objects.create(
                member=member,
                email_type='birthday',
                status='failed',
                error_message=str(e),
                email_subject=subject if 'subject' in locals() else 'Birthday Wish'
            )
            
            failed_count += 1
            logger.error(f"Failed to send birthday wish to {member.email}: {str(e)}")
    
    logger.info(f"Birthday wishes completed: {sent_count} sent, {failed_count} failed")
    return {'sent': sent_count, 'failed': failed_count}


@shared_task
def send_inactivity_alerts(member_ids=None, force_send=False):
    """
    Send inactivity alerts to members who haven't checked in for 7+ days
    """
    today = date.today()
    inactive_threshold = today - timedelta(days=7)
    
    # Get members who haven't checked in for 7+ days
    queryset = Member.objects.filter(
        is_active=True,
        last_checkin_date__lt=inactive_threshold
    )
    
    if member_ids:
        queryset = queryset.filter(id__in=member_ids)
    
    sent_count = 0
    failed_count = 0
    
    for member in queryset:
        # Check if we've already sent an inactivity alert recently (unless force_send)
        if not force_send:
            recent_log = EmailLog.objects.filter(
                member=member,
                email_type='inactivity',
                status='sent',
                sent_date__gte=today - timedelta(days=7)
            ).exists()
            
            if recent_log:
                logger.info(f"Skipping {member.email} - inactivity alert already sent recently")
                continue
        
        try:
            # Prepare email content
            context = {
                'member': member,
                'days_since_checkin': member.days_since_checkin,
                'frontend_url': settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:5173',
            }
            
            subject = "We Miss You! Come Back to the Gym"
            html_content = render_to_string('emails/inactivity_alert.html', context)
            text_content = render_to_string('emails/inactivity_alert.txt', context)
            
            # Send email
            send_mail(
                subject=subject,
                message=text_content,
                from_email=f"{settings.DEFAULT_FROM_NAME} <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[member.email],
                html_message=html_content,
                fail_silently=False,
            )
            
            # Log successful send
            EmailLog.objects.create(
                member=member,
                email_type='inactivity',
                status='sent',
                email_subject=subject,
                email_content=html_content
            )
            
            sent_count += 1
            logger.info(f"Inactivity alert sent to {member.email}")
            
        except Exception as e:
            # Log failed send
            EmailLog.objects.create(
                member=member,
                email_type='inactivity',
                status='failed',
                error_message=str(e),
                email_subject=subject if 'subject' in locals() else 'Inactivity Alert'
            )
            
            failed_count += 1
            logger.error(f"Failed to send inactivity alert to {member.email}: {str(e)}")
    
    logger.info(f"Inactivity alerts completed: {sent_count} sent, {failed_count} failed")
    return {'sent': sent_count, 'failed': failed_count}