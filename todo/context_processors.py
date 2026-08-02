from .models import Notification
from datetime import date

def notification_count(request):
    """تعداد اعلان‌های خوانده‌نشدهٔ کاربر جاری را به تمام قالب‌ها تزریق می‌کند."""
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        count = 0
    today = date.today()
    return {'unread_notifications_count': count,'today':today}


import os

def use_redis(request):
    return {'USE_REDIS': os.environ.get('USE_REDIS', 'True').lower() == 'true'}