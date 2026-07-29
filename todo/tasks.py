# from celery import shared_task
# from .models import Todo



# @shared_task
# def debug_task():
#     print('=' * 50)
#     print('✅ Celery Worker is alive and working!')
#     print('=' * 50)
#     return "Task completed successfully"

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Todo

@shared_task
def send_due_date_reminders():
    today = timezone.localdate()
    todos = Todo.objects.filter(due_date=today, status__in=['SE', 'DN']).select_related('assign_to')
    user_tasks = {}
    for todo in todos:
        user_tasks.setdefault(todo.assign_to, []).append(todo.name)
    for user, tasks in user_tasks.items():
        if user.email:
            send_mail(
                'یادآوری تسک‌های امروز',
                f'تسک‌های زیر امروز سررسید دارند:\n' + '\n'.join(tasks),
                'noreply@todo.local',
                [user.email],
                fail_silently=False,
            )


from datetime import timedelta
from .models import Notification

@shared_task
def cleanup_old_notifications():
    """
    اعلان‌هایی که بیش از ۳۰ روز از ایجادشان گذشته و خوانده شده‌اند را حذف می‌کند.
    """
    cutoff = timezone.now() - timedelta(days=1)
    deleted_count, _ = Notification.objects.filter(
        created__lt=cutoff,
        is_read=True
    ).delete()
    
    print(f"پاک‌سازی انجام شد. {deleted_count} اعلان قدیمی حذف شدند.")
    return deleted_count


@shared_task
def test_email():
    from django.core.mail import send_mail
    send_mail(
        'Test Subject',
        'Test Body',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )
    print("Email sent successfully")



@shared_task
def test_websocket_message(user_id):
    """
    یک پیام تستی به WebSocket کاربر ارسال می‌کند.
    """
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{user_id}',
        {
            'type': 'send_notification',
            'data': {
                'message': 'پیام تستی از WebSocket',
                'unread_count': 999,
            }
        }
    )