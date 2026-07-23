import os
from celery import Celery

# تنظیم متغیر محیطی پیش‌فرض برای تنظیمات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# خواندن تنظیمات از settings.py با پیشوند CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# کشف خودکار Taskها در همهٔ اپ‌ها
app.autodiscover_tasks()