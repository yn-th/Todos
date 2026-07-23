from celery import shared_task
from .models import Todo



@shared_task
def debug_task():
    print('=' * 50)
    print('✅ Celery Worker is alive and working!')
    print('=' * 50)
    return "Task completed successfully"