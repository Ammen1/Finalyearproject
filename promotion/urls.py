from django.urls import path
from . import views

app_name = 'promotion'

urlpatterns = [
    path('list/', views.promotion_list, name='promotion_list'),
    path('detail/<int:pk>/', views.promotion_detail, name='promotion_detail'),
]
