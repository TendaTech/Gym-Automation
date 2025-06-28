import django_filters
from django.db.models import Q
from datetime import date, timedelta
from .models import Member


class MemberFilter(django_filters.FilterSet):
    # Status filters
    status = django_filters.ChoiceFilter(
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('due_soon', 'Due Soon'),
            ('overdue', 'Overdue'),
        ],
        method='filter_by_status'
    )
    
    # Date range filters
    subscription_due_after = django_filters.DateFilter(
        field_name='subscription_due_date',
        lookup_expr='gte'
    )
    subscription_due_before = django_filters.DateFilter(
        field_name='subscription_due_date',
        lookup_expr='lte'
    )
    
    # Birthday filters
    birthday_today = django_filters.BooleanFilter(method='filter_birthday_today')
    birthday_this_week = django_filters.BooleanFilter(method='filter_birthday_this_week')
    birthday_this_month = django_filters.BooleanFilter(method='filter_birthday_this_month')
    
    # Check-in filters
    last_checkin_after = django_filters.DateFilter(
        field_name='last_checkin_date',
        lookup_expr='gte'
    )
    last_checkin_before = django_filters.DateFilter(
        field_name='last_checkin_date',
        lookup_expr='lte'
    )
    
    # Membership type
    membership_type = django_filters.MultipleChoiceFilter(
        choices=Member.MEMBERSHIP_TYPES
    )

    class Meta:
        model = Member
        fields = {
            'is_active': ['exact'],
            'full_name': ['icontains'],
            'email': ['icontains'],
            'phone': ['icontains'],
        }

    def filter_by_status(self, queryset, name, value):
        today = date.today()
        
        if value == 'active':
            return queryset.filter(is_active=True)
        elif value == 'inactive':
            return queryset.filter(is_active=False)
        elif value == 'due_soon':
            due_soon_date = today + timedelta(days=5)
            return queryset.filter(
                subscription_due_date__gte=today,
                subscription_due_date__lte=due_soon_date,
                is_active=True
            )
        elif value == 'overdue':
            return queryset.filter(
                subscription_due_date__lt=today,
                is_active=True
            )
        
        return queryset

    def filter_birthday_today(self, queryset, name, value):
        if value:
            today = date.today()
            return queryset.filter(
                birthday__month=today.month,
                birthday__day=today.day
            )
        return queryset

    def filter_birthday_this_week(self, queryset, name, value):
        if value:
            today = date.today()
            week_end = today + timedelta(days=7)
            
            # Handle year boundary
            if today.year == week_end.year:
                return queryset.filter(
                    Q(birthday__month=today.month, birthday__day__gte=today.day) |
                    Q(birthday__month=week_end.month, birthday__day__lte=week_end.day)
                )
            else:
                return queryset.filter(
                    Q(birthday__month=today.month, birthday__day__gte=today.day) |
                    Q(birthday__month=week_end.month, birthday__day__lte=week_end.day)
                )
        return queryset

    def filter_birthday_this_month(self, queryset, name, value):
        if value:
            today = date.today()
            return queryset.filter(birthday__month=today.month)
        return queryset