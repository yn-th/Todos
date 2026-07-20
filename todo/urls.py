from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views


router  = DefaultRouter()
router.register(r'todos',views.TodoViewSet,basename='todo')

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('',views.home),
    path('',views.TodoListView.as_view(),name='home'),
    path('create/',views.TodoCreateView.as_view(),name = 'create'),
    path('feed/', views.UserFeedView.as_view(), name='user_feed'),
    path('user/<int:pk>/follow/', views.toggle_follow, name='toggle_follow'),

    path('update/<str:slug>',views.TodoUpdateView.as_view(),name = 'update'),
    path('detail/<str:slug>',views.TodoDetailView.as_view() , name='detail'),
    path('delete/<str:slug>',views.TodoDeleteView.as_view() , name='delete'),
    path('todo/<int:pk>/change-status/', views.change_status, name='change_status'),
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('users/',views.UserListView.as_view(), name='user_list'),
###################-----API----###########################################
    path('api/todos/', views.TodoListAPI.as_view(), name='todo_api_list'),
    path('api/todos/<str:slug>/', views.TodoDetailAPI.as_view(), name='todo_api_detail'),
]
