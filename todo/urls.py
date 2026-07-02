from django.urls import path
from . import views

urlpatterns = [
   
    path('',views.home),
    path('detail/<slug>',views.detail , name= 'detail')
]
