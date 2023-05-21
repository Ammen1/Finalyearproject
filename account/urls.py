from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from . import StaffViews, HodViews


from . import views
from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm


app_name = "account"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/login.html", form_class=UserLoginForm),
        name="login",
    ),
    path("logoutUser/", auth_views.LogoutView.as_view(next_page="/account/login/"), name="logoutUser"),
    path("register/", views.account_register, name="register"),
    path("activate/<slug:uidb64>/<slug:token>)/", views.account_activate, name="activate"),
    # Reset password
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset/password_reset_form.html",
            success_url="password_reset_email_confirm",
            email_template_name="account/password_reset/password_reset_email.html",
            form_class=PwdResetForm,
        ),
        name="pwdreset",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset/password_reset_confirm.html"
        ,success_url="password_reset_complete/",form_class=PwdResetConfirmForm,),
        name="password_reset_confirm",
    ),
    path("password_reset/password_reset_email_confirm/",TemplateView.as_view(template_name="account/password_reset/reset_status.html"),name="password_reset_done",),
    path("password_reset_confirm/Mg/password_reset_complete/",TemplateView.as_view(template_name="account/password_reset/reset_status.html"),name="password_reset_complete",),
    # # User dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/edit/", views.edit_details, name="edit_details"),
    path("profile/delete_user/", views.delete_user, name="delete_user"),
    path("profile/delete_confirm/",TemplateView.as_view(template_name="account/dashboard/delete_confirm.html"),name="delete_confirmation",),
    path("addresses/", views.view_address, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.set_default, name="set_default"),
    path("user_orders/", views.user_orders, name="user_orders"),
    # path('admin_home/', HodViews.admin_home, name="admin_home"),
    # path('add_staff/', HodViews.add_staff, name="add_staff"),
    # path('add_staff_save/', HodViews.add_staff_save, name="add_staff_save"),
    # path('manage_staff/', HodViews.manage_staff, name="manage_staff"),
    # path('edit_staff/<staff_id>/', HodViews.edit_staff, name="edit_staff"),
    # path('edit_staff_save/', HodViews.edit_staff_save, name="edit_staff_save"),
    # path('delete_staff/<staff_id>/', HodViews.delete_staff, name="delete_staff"),
    # path('check_email_exist/', HodViews.check_email_exist, name="check_email_exist"),
    # path('check_username_exist/', HodViews.check_username_exist, name="check_username_exist"),
    # path('users_feedback_message/', HodViews.users_feedback_message, name="users_feedback_message"),
    # path('users_feedback_message_reply/', HodViews.users_feedback_message_reply, name="users_feedback_message_reply"),
    # path('staff_feedback_message/', HodViews.staff_feedback_message, name="staff_feedback_message"),
    # path('staff_feedback_message_reply/', HodViews.staff_feedback_message_reply, name="staff_feedback_message_reply"),
    # path('staff_leave_view/', HodViews.staff_leave_view, name="staff_leave_view"),
    # path('staff_leave_approve/<leave_id>/', HodViews.staff_leave_approve, name="staff_leave_approve"),
    # path('staff_leave_reject/<leave_id>/', HodViews.staff_leave_reject, name="staff_leave_reject"),
    # path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    # path('admin_profile_update/', HodViews.admin_profile_update, name="admin_profile_update"),

    #     # URLS for Staff
    # path('staff_home/', StaffViews.staff_home, name="staff_home"),
    # path('staff_apply_leave/', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    # path('staff_apply_leave_save/', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    # path('staff_feedback/', StaffViews.staff_feedback, name="staff_feedback"),
    # path('staff_feedback_save/', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    # path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
    # path('staff_profile_update/', StaffViews.staff_profile_update, name="staff_profile_update"),
    
 
]
