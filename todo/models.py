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
        DONE = 'DO','انجام شده'
        DOING = 'DN' , 'در حال انجام'
        SEE = 'SE' , 'دیده شده '
    
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.SEE
        )
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created']