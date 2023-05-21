from django.urls import path
from .views import index
app_name = "map"

urlpatterns = [
    path('index/', index, name='index'),
]
