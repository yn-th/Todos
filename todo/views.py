from django.shortcuts import render ,get_object_or_404
from .models import Todo
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    todos = Todo.objects.all()
    return render(request , 'todo/index.html',{'todos':todos})
    

def detail(request , slug):
    todo = get_object_or_404(Todo,slug=slug)
    return render(request , 'todo/detail.html',{'todo':todo})


def dashboard(request):
    todos = Todo.objects.filter(assign_to =request.user)
    print(User)
    return render(request , 'todo/dashboard.html',{'todos':todos})


