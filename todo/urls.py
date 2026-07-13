from django.urls import path
from .views import change_status,TodoListView,TodoDeleteView , TodoDetailView, TodoCreateView,TodoUpdateView

urlpatterns = [
   
    # path('',views.home),
    path('',TodoListView.as_view(),name='home'),
    path('create/',TodoCreateView.as_view(),name = 'create'),
    path('update/<str:slug>',TodoUpdateView.as_view(),name = 'update'),
    path('detail/<str:slug>',TodoDetailView.as_view() , name='detail'),
    path('delete/<str:slug>',TodoDeleteView.as_view() , name='delete'),
    path('todo/<int:pk>/change-status/', change_status, name='change_status'),
    
    # path('dashboard',dashboard,name='dashboard'),
]
