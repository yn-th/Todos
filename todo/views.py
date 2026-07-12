from django.shortcuts import render ,get_object_or_404 , redirect
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoCrateForm
from django.views.generic import ListView , DetailView , CreateView ,UpdateView ,DeleteView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

    
class TodoListView(LoginRequiredMixin,ListView):
    model = Todo
    template_name = "todo/index.html"
    context_object_name = 'todos'
    paginate_by = 6
    
    def get_queryset(self):
        queryset= super().get_queryset()
        queryset = queryset.filter(assign_to =self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)|Q(body__icontains=query)
            )
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(Q(priority__icontains = priority))
        
        return queryset.order_by('-created')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get('q','') 
        context['selected_priority'] = self.request.GET.get('priority', '')
        return context
    
    

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

class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "todo/delete_confirm.html"
    success_url = reverse_lazy('home')







# def detail(request , slug):
#     todo = get_object_or_404(Todo,slug=slug)
#     return render(request , 'todo/detail.html',{'todo':todo})


def dashboard(request):
    todos = Todo.objects.filter(assign_to =request.user)
    print(User)
    return render(request , 'todo/dashboard.html',{'todos':todos})


