from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class Todoserializers(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    assign_to_detail = UserSerializer(source='assign_to', read_only=True)
    assign_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = Todo
        fields = ['id','name','body','priority','status',
                  'due_date','is_public','days_since_created',
                  'assign_to','assign_to_detail',
                  ]
    
    def get_days_since_created(self, obj):
        from datetime import date
        if obj.created:
            delta = date.today() - obj.created.date()
            return delta.days
        return None