from django.urls import path
from . import views

app_name = 'privetchat'

urlpatterns = [
   
    path('home/', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]








# from django.urls import path

# from . import views

# app_name = 'privetchat'

# urlpatterns = [
#     path('home/', views.home, name='home'),
#     path('chat/<int:sender_id>/<int:receiver_id>/', views.chat_between_users, name='chat_between_users'),
# ]
