from rest_framework import serializers
from .models import Todo

class Todoserializers(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id','name','body','priority','status','due_date','is_public','assign_to']
        