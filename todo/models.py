from django.db import models

# Create your models here.

class Todo(models.Model):
    name = models.CharField( max_length=250)
    todo = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Priority(models.TextChoices):
        HIGH = 'H' , 'بالا'
        MEDIUM = 'M' , 'متوسط'
        LOW = 'L' , 'پایین'

    priority = models.CharField( max_length=1,choices=Priority,default=Priority.MEDIUM)

    class Status(models.TextChoices):
        DONE = 'DO','انجام شده'
        DOING = 'DN' , 'در حال انجام'
        SEE = 'SE' , 'دیده شده '
    
    
