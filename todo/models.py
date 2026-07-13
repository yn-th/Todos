from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Todo(models.Model):
    name = models.CharField( max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True,unique=True,blank=True)
    due_date = models.DateField(null=True, blank=True, verbose_name="تاریخ سررسید")
    assign_to = models.ForeignKey(
        User,
        related_name='todo',
        on_delete=models.CASCADE
        )
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name,allow_unicode=True)
    #     return super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            if not base_slug:                # اگر slugify خالی برگرداند
                base_slug = 'todo'
            # یکتا‌سازی: اگر slug تکراری بود، شماره اضافه کن
            unique_slug = base_slug
            counter = 1
            while Todo.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
    class Priority(models.TextChoices):
        HIGH = 'H' , 'بالا'
        MEDIUM = 'M' , 'متوسط'
        LOW = 'L' , 'پایین'

    priority = models.CharField( max_length=1,choices=Priority,default=Priority.MEDIUM)

    class Status(models.TextChoices):
        NEW = 'NE','-------'
        DONE = 'DO','انجام شده'
        DOING = 'DN' , 'در حال انجام'
        SEE = 'SE' , 'دیده شده '
    
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.NEW
        )
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created']


class Notification(models.Model):
    message = models.CharField(max_length=550)
    user = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE
        )
    created = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    link = models.CharField( max_length=250)

    def __str__(self):
        return f"{self.user} - {self.message}"
