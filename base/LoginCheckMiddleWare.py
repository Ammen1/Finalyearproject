from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse



class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        print(modulename)
        user = request.user

        #Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "base.HodViews":
                    pass
                elif modulename == "base.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("admin_home")
            
            elif user.user_type == "2":
                if modulename == "base.UserViews":
                    pass
                elif modulename == "base.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("doctor_home")
            
            elif user.user_type == "3":
                if modulename == "base.UserViews":
                    pass
                elif modulename == "base.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("user_home")

            else:
                return redirect("login")

        else:
            if request.path == reverse("login") or request.path == reverse("doLogin"):
                pass
            else:
                return redirect("login")
