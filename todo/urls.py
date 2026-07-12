from django.urls import path
from .views import TodoListView,dashboard , TodoDetailView, TodoCreateView,TodoUpdateView

urlpatterns = [
   
    # path('',views.home),
    path('',TodoListView.as_view(),name='home'),
    path('create/',TodoCreateView.as_view(),name = 'create'),
    path('update/<slug:slug>',TodoUpdateView.as_view(),name = 'update'),
    path('detail/<slug:slug>',TodoDetailView.as_view() , name='detail'),
    
    path('dashboard',dashboard,name='dashboard'),
]
