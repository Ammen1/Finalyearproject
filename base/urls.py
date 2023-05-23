from django.urls import path
from . import views
from .views import doctor_list, doctor_detail
app_name = 'base'

urlpatterns = [


    path('', views.hospital_all, name='store_home'),
    path('hospital_all/', views.hospital_all, name='hospital_all'),
    path('dashboard-index/', views.index, name='dashboard-index'),
    # path('hospital/<slug:slug>/', views.map, name='hospital_map'),
    path('hospital<slug:slug>', views.hospital_detail, name='hospital_detail'),
    path('hospital/<slug:category_slug>/', views.category_list, name='category_list'),
    path('save_location/',views.save_location, name='save_location'),
    path('doctor-list/', doctor_list, name='doctor_list'),
    path('doctor-detail/<slug:slug>/', doctor_detail, name='doctor_detail'),
    path('staff_apply_leave/', views.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save/', views.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback/', views.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save/', views.staff_feedback_save, name="staff_feedback_save"),
    path('users_feedback_message/', views.users_feedback_message, name="users_feedback_message"),
    path('users_feedback_message_reply/', views.users_feedback_message_reply, name="users_feedback_message_reply"),
    path('staff_feedback_message/', views.staff_feedback_message, name="staff_feedback_message"),
    path('staff_feedback_message_reply/', views.staff_feedback_message_reply, name="staff_feedback_message_reply"),
    path('staff_leave_view/', views.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/', views.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/', views.staff_leave_reject, name="staff_leave_reject"),
    path('users_feedback/', views.users_feedback, name="users_feedback"),
    path('users_feedback_save/', views.users_feedback_save, name="users_feedback_save"),
    path("services/", views.services, name="services"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('users_message/', views.users_message, name="users_message"),
    path('users_message_save/', views.users_message_save, name="users_message_save"),
    path('users_message_view/', views.users_message_view, name="users_message_view"),
    path('users_message_reply/', views.users_message_reply, name="users_message_reply"),


    
]
