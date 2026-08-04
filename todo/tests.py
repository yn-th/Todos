from django.test import TestCase , override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from .models import Todo

# Create your tests here.


class TodoViewSetTest(APITestCase):
    
    def setUp(self):
        
        self.user1 = User.objects.create(
            username = 'ali',
            password = 'pass1234',
        )
        self.user2 = User.objects.create(
            username = 'sara',
            password = 'pass4567',
        )

        self.todo1 = Todo.objects.create(
            name = "ali task",
            body = "this is frist test",
            assign_to = self.user1,
            status = 'SE',

        ) 
        self.todo2 = Todo.objects.create(
            name = "sara task",
            body = "this is second test",
            assign_to = self.user2,
            status = 'DN',

        ) 

        self.list_url = reverse('todo-list')
        self.detail_url = reverse('todo-detail',kwargs={'slug':self.todo1.slug})

    def test_guest_cannot_access_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code ,status.HTTP_401_UNAUTHORIZED)

    def test_guest_cannot_access_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_only_own_tasks(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.todo1.name)

    def test_create_task_sets_assignee(self):
        self.client.force_authenticate(user = self.user1)
        data = {
            'name':'new task',
            'body':'this is new task for ali',
            'priority':'H',
            'status':'SE',
            }
        response = self.client.post(self.list_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['assign_to'],self.user1)
    
    def test_cannot_edit_others_task(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(self.detail_url, {'name': 'هک شده'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_delete(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(slug=self.todo1.slug).exists())



from .tasks import debug_task

class CeleryTaskTest(TestCase):
    
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_debug_task_runs_successfully(self):
        """تست می‌کنیم که debug_task بدون خطا اجرا شود و پیام درست را برگرداند."""
        result = debug_task.delay()
        self.assertTrue(result.successful())
        self.assertEqual(result.result, "Task completed successfully")


from .tasks import send_due_date_reminders

class CeleryTaskTest(TestCase):
    
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_send_reminder_for_today_tasks(self):
        """تسکی با سررسید امروز باید باعث ارسال ایمیل شود."""
        # ۱. ساخت یک کاربر با ایمیل معتبر
        user = User.objects.create_user(username='testuser', email='test@example.com')
        
        # ۲. ساخت یک تسک با سررسید امروز و وضعیت SE
        Todo.objects.create(
            name='تسک تستی',
            due_date=date.today(),
            status='SE',
            assign_to=user
        )
        
        # ۳. اجرای Task
        result = send_due_date_reminders.delay()
        
        # ۴. بررسی موفقیت Task
        self.assertTrue(result.successful())
        
        # ۵. بررسی اینکه یک ایمیل ارسال شده است
        from django.core import mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('تسک تستی', mail.outbox[0].body)


from datetime import timedelta
from django.utils import timezone
from .models import Notification
from .tasks import cleanup_old_notifications

class CeleryTaskTest(TestCase):
    
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_cleanup_old_notifications(self):
        user = User.objects.create_user(username='testuser2')
        
        # ۱. ساخت یک اعلان قدیمی (۳۵ روز پیش)
        old_notif = Notification.objects.create(
            user=user,
            message='اعلان قدیمی',
            is_read=True
        )
        old_notif.created = timezone.now() - timedelta(days=35)
        old_notif.save()
        
        # ۲. ساخت یک اعلان جدید
        Notification.objects.create(
            user=user,
            message='اعلان جدید',
            is_read=True
        )
        
        # ۳. اجرای Task
        result = cleanup_old_notifications.delay()
        self.assertTrue(result.successful())
        
        # ۴. فقط اعلان قدیمی باید حذف شده باشد
        self.assertFalse(Notification.objects.filter(message='اعلان قدیمی').exists())
        self.assertTrue(Notification.objects.filter(message='اعلان جدید').exists())
        self.assertEqual(result.result, 1)  # تعداد حذف‌شده