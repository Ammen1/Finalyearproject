from django.urls import  path

from . import views

app_name = "checkout"

urlpatterns = [
    path("servicechoices", views.servicechoices, name="servicechoices"),
    path("basket_update_service/", views.basket_update_service, name="basket_update_service"),
    path("service_address/", views.service_address, name="service_address"),
    path("payment_selection/", views.payment_selection, name="payment_selection"),
    path("payment_complete/", views.payment_complete, name="payment_complete"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),
 ]
