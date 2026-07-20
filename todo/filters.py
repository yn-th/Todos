import django_filters
from .models import Todo

class TodoFilter(django_filters.FilterSet):
    # فیلتر بازه‌ای برای تاریخ سررسید
    due_date_from = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')
    due_date_to = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')

    class Meta:
        model = Todo
        fields = {
            'priority': ['exact'],           # ?priority=H
            'status': ['exact'],             # ?status=DO
            'is_public': ['exact'],          # ?is_public=True
            'assign_to': ['exact'],          # ?assign_to=1
        }