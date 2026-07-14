from django.contrib import admin
from .models import Todo , Notification
# Register your models here.
@admin.register(Todo)

class AdminTodo(admin.ModelAdmin):
    list_display = ['name','body','priority','status','slug','assign_to','is_public']
    prepopulated_fields ={'slug':('name',)}
    list_editable=['status','priority','is_public']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user','message','link','is_read']    
