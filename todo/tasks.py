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
        else:
            print('kos nnanaat')

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