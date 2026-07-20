from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # obj همون شیء Todo هست که می‌خوایم بررسیش کنیم
        return obj.assign_to == request.user