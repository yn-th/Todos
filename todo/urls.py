from django.urls import path
from . import views

urlpatterns = [
   
    path('',views.home),
    path('detail/<slug>',views.detail , name= 'detail'),
    path('dashboard',views.dashboard,name='dashboard'),
]
