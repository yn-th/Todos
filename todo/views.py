from django.shortcuts import render ,get_object_or_404 , redirect
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoCrateForm
from django.views.generic import ListView , DetailView , CreateView ,UpdateView
from django.contrib.auth.models import User
# Create your views here.

# def home(request):
#     todos = Todo.objects.all()
#     return render(request , 'todo/index.html',{'todos':todos})
    
class TodoListView(ListView):
    model = Todo
    template_name = "todo/index.html"
    context_object_name = 'todos'
    paginate_by = 6

class TodoDetailView(DetailView):
    model = Todo
    template_name = "todo/detail.html"
    slug_field = 'slug'
    context_object_name = 'todo'

class TodoCreateView(CreateView):
    model = Todo
    form_class = TodoCrateForm
    template_name = "todo/create.html"
    success_url = reverse_lazy('home')
    
class TodoUpdateView(UpdateView):
    model = Todo
    template_name = "todo/update.html"
    success_url = reverse_lazy('home')
    form_class = TodoCrateForm





# def detail(request , slug):
#     todo = get_object_or_404(Todo,slug=slug)
#     return render(request , 'todo/detail.html',{'todo':todo})


def dashboard(request):
    todos = Todo.objects.filter(assign_to =request.user)
    print(User)
    return render(request , 'todo/dashboard.html',{'todos':todos})


