from django.db.models.signals import post_save , post_init
from django.dispatch import receiver 
from django.contrib.auth.models import User
from .models import Todo , Notification

@receiver(post_save , sender=Todo)

def create_todo_notif(sender ,instance, created , **kwargs):
    if created:
        Notification.objects.create(
            user = instance.assign_to,
            message = f"تسک جدیدی به شما ارسال شده است{instance.name}",
            link=f'/detail/{instance.slug}' 
        )


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

            
