from django.shortcuts import render ,get_object_or_404 , redirect 
from django.urls import reverse_lazy 
from .models import Todo,Contact
from .forms import TodoCrateForm
from django.views.generic import ListView , DetailView , CreateView ,UpdateView ,DeleteView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse ,Http404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def change_status(request, pk):
    todo = get_object_or_404(Todo, pk=pk, assign_to=request.user)

    new_status = request.POST.get('status')

    valid_statuses = [choice[0] for choice in Todo.Status.choices]
    if new_status not in valid_statuses:
        return JsonResponse({'success': False, 'error': 'وضعیت نامعتبر است.'}, status=400)

    todo.status = new_status
    todo.save()
    return JsonResponse({
        'success': True,
        'new_status': todo.get_status_display(),  # نمایش فارسی
        'new_status_code': todo.status             # کد وضعیت (SE, DN, DO)
    })
    
class TodoListView(LoginRequiredMixin,ListView):
    model = Todo
    template_name = "todo/index.html"
    context_object_name = 'todos'
    paginate_by = 6
    
    def get_queryset(self):
        queryset= super().get_queryset()
        queryset = queryset.select_related('assign_to')
        queryset = queryset.filter(assign_to = self.request.user)
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
    
    

class TodoDetailView(LoginRequiredMixin,DetailView):
    model = Todo
    template_name = "todo/detail.html"
    slug_field = 'slug'
    context_object_name = 'todo'
    
    def get_queryset(self):
        return super().get_queryset().select_related('assign_to').filter(
            assign_to = self.request.user
        )
    

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
    def get_queryset(self):
        return super().get_queryset().filter(assign_to=self.request.user)

class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "todo/delete_confirm.html"
    success_url = reverse_lazy('home')
    def get_queryset(self):
        return super().get_queryset().filter(assign_to=self.request.user)






# def detail(request , slug):
#     todo = get_object_or_404(Todo,slug=slug)
#     return render(request , 'todo/detail.html',{'todo':todo})

from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'todo/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created')

from django.contrib import messages

@login_required
def mark_all_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        messages.success(request, 'همهٔ اعلان‌ها خوانده شدند.')
    return redirect('notification_list')



@login_required
@require_POST
def toggle_follow(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    
    if request.user == target_user:
        return JsonResponse({
            'success': False,
            'error': 'نمی‌توانید خودتان را دنبال کنید.'
        }, status=400)

    # بررسی می‌کنیم که آیا رابطه از قبل وجود دارد
    contact = Contact.objects.filter(user_from=request.user, user_to=target_user).first()
    
    if contact:
        contact.delete()
        followed = False
    else:
        Contact.objects.create(user_from=request.user, user_to=target_user)
        followed = True

    return JsonResponse({
        'success': True,
        'followed': followed,
        'follower_count': target_user.rel_to_set.count() 
    })

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'todo/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        # کاربر جاری را از لیست حذف می‌کنیم
        return User.objects.exclude(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # کاربرانی که کاربر جاری دنبال می‌کند
        following_ids = Contact.objects.filter(
            user_from=self.request.user
        ).values_list('user_to', flat=True)
        context['following_ids'] = list(following_ids)
        return context


class UserFeedView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/feed.html'
    context_object_name = 'todos'
    paginate_by = 10

    def get_queryset(self):
        # ۱. لیست کاربرانی که کاربر جاری دنبال می‌کند
        following_ids = Contact.objects.filter(
            user_from=self.request.user
        ).values_list('user_to_id', flat=True)

        # ۲. تسک‌های عمومی آن کاربران + تسک‌های عمومی خود کاربر
        return Todo.objects.filter(
            assign_to__in=list(following_ids) + [self.request.user.id],
            is_public=True,
            status__in=[Todo.Status.SEE, Todo.Status.DOING, Todo.Status.DONE]
        ).select_related('assign_to').order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_title'] = 'فید تسک‌های دنبال‌شده'
        return context

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Todoserializers

class TodoListAPI(APIView):
    pass
#     def get(self,request):
#         todos = Todo.objects.all()
#         serializers = Todoserializers(todos , many = True)
#         return Response(serializers.data)
    
#     def post(self , request):
#         serializer = Todoserializers(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=201)
#         return Response(serializer.errors,status=400)

# class TodoDetailAPI(APIView):
#     def get_object(self,slug):
#         try:
#             return Todo.objects.get(slug=slug)
#         except Todo.DoesNotExist:
#             raise Http404

#     def get(self , request , slug):
#         todo = self.get_object(slug)
#         serializer = Todoserializers(todo)
#         return Response(serializer.data)
#     def put(self,request,slug):
#         todo = self.get_object(slug)
#         serializer = Todoserializers(todo, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=400)
#     def delete(self,request,slug):
#         todo = self.get_object(slug)
#         todo.delete()
#         return Response(status=204)
    

from rest_framework.generics import RetrieveUpdateDestroyAPIView

class TodoDetailAPI(RetrieveUpdateDestroyAPIView):
    pass
#     queryset = Todo.objects.all()
#     serializer_class = Todoserializers
#     lookup_field = 'slug'


from rest_framework.generics import ListCreateAPIView
from rest_framework import filters 

class TodoListAPI(ListCreateAPIView):
    pass
#     queryset = Todo.objects.all()
#     serializer_class = Todoserializers
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['name','body']
#     # pagination_class = pagination

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         priority = self.request.GET.get('priority')
#         if priority:
#             queryset = queryset.filter(priority=priority)

#         return queryset
    

# from rest_framework import viewsets
# from datetime import date
# from .permissions import IsOwner

# class TodoViewSet(viewsets.ModelViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = Todoserializers
#     lookup_field = 'slug'
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['name','body']
#     permission_classes = [IsOwner]
#     def get_queryset(self):
#         queryset= super().get_queryset()
#         priority = self.request.GET.get('priority')
#         if priority:
#             queryset = queryset.filter(priority=priority)

#         return queryset


from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from datetime import date
from .models import Todo
from .serializers import Todoserializers
from .permissions import IsOwner
from .filters import TodoFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = Todoserializers
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['name', 'body']
    filterset_class = TodoFilter

    def get_permissions(self):
        # برای اعمال Permission های مختلف به Action های متفاوت
        if self.action in ['list', 'create']:
            self.permission_classes = [IsAuthenticated]
        else:  # retrieve, update, partial_update, destroy
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()

    def get_queryset(self):
        return Todo.objects.filter(assign_to=self.request.user).order_by('-created')
     

    def perform_create(self, serializer):
        # خودکار assign_to را پر کن
        serializer.save(assign_to=self.request.user)

    @action(detail=True, methods=['post'], url_path='mark-done')
    def mark_done(self, request, slug=None):
      
        todo = self.get_object()  # به‌طور خودکار شیء را با lookup_field (slug) پیدا می‌کند
        todo.status = Todo.Status.DONE
        todo.save()
        return Response({'status': 'تسک با موفقیت انجام شد.', 'new_status': todo.get_status_display()})