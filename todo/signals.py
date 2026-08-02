from django.db.models.signals import post_save , post_init
from django.dispatch import receiver 
from django.contrib.auth.models import User
from .models import Todo , Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save , sender=Todo)

def create_todo_notif(sender ,instance, created , **kwargs):
    print(f"SIGNAL TRIGGERED: Todo created for user {instance.assign_to.id}")
    if created:
        notification = Notification.objects.create(
        user=instance.assign_to,
        message=f"تسک جدیدی به شما ارسال شده است: {instance.name}",
        link=f'/detail/{instance.slug}'
    )
    print(f"Notification created for user {notification.user.id}")

    channel_layer = get_channel_layer()
    group_name = f'user_{notification.user.id}'
    print(f"Sending to group: {group_name}")

    try:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                'data': {
                    'message': notification.message,
                    'unread_count': Notification.objects.filter(
                        user=notification.user, is_read=False
                    ).count(),
                }
            }
        )
        print(f"Message sent successfully to group {group_name}")
    except Exception as e:
        print(f"ERROR sending to group {group_name}: {e}")
#         notification =  Notification.objects.create(
#             user = instance.assign_to,
#             message = f"تسک جدیدی به شما ارسال شده است{instance.name}",
#             link=f'/detail/{instance.slug}' 
#         )
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f'user_{notification.user.id}',
#     {
#         'type': 'send_notification',
#         'data': {
#             'message': notification.message,
#             'unread_count': Notification.objects.filter(user=notification.user, is_read=False).count(),
#         }
#     }
# )



@receiver(post_init , sender=Todo)

def store_pre_status(sender , instance , **kwargs):
    instance._old_status = instance.status

@receiver(post_save , sender=Todo)
def change_todo_status(sender,instance,created,**kwargs):
    if not created:
        old_status = getattr(instance , '_old_status',None)
        new_status = instance.status
        if old_status and old_status != new_status:
            Notification.objects.create(
                user = instance.assign_to,
                message=f'وضعیت تسک "{instance.name}" از "{old_status}" به "{new_status}" تغییر کرد.',
                link=f'/detail/{instance.slug}'
            )

            
