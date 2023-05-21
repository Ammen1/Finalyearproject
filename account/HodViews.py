# from base.models import Doctors,Users, FeedBackUser, FeedBackDoctors, LeaveReportDoctors
# from .models import Customer,Address
# from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import cache_control
# from django.core.files.storage import FileSystemStorage #To upload Profile Picture
# from django.urls import reverse
# from django.views.decorators.csrf import csrf_exempt
# from django.core import serializers
# from base.models import Hospital

# import json


# @login_required(login_url='login')
# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# def admin_home(request):
#     all_hospital_count = Hospital.objects.all().count()
#     return render(request, "hod_template/home_content.html", {'all_hospital_count':all_hospital_count})


# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def add_staff(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     return render(request, "hod_template/add_staff_template.html")

# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def add_staff_save(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     if request.method != "POST":
#         messages.error(request, "Invalid Method ")
#         return redirect('add_staff')
#     else:
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         address = request.POST.get('address')

#         try:
#             user = Doctors.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
#             user.staffs.address = address
#             user.save()
#             messages.success(request, "Staff Added Successfully!")
#             return redirect('add_staff')
#         except:
#             messages.error(request, "Failed to Add Staff!")
#             return redirect('add_staff')



# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def manage_staff(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     staffs = Doctors.objects.all()
#     context = {
#         "staffs": staffs
#     }
#     return render(request, "hod_template/manage_staff_template.html", context)

# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def edit_staff(request, staff_id):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     staff = Doctors.objects.get(admin=staff_id)

#     context = {
#         "staff": staff,
#         "id": staff_id
#     }
#     return render(request, "hod_template/edit_staff_template.html", context)

# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def edit_staff_save(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     if request.method != "POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
#         staff_id = request.POST.get('staff_id')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         address = request.POST.get('address')

#         try:
#             # INSERTING into user Model
#             user = User.objects.get(id=staff_id)
#             user.first_name = first_name
#             user.last_name = last_name
#             user.email = email
#             user.username = username
#             user.save()
            
#             # INSERTING into Staff Model
#             staff_model = Doctors.objects.get(admin=staff_id)
#             staff_model.address = address
#             staff_model.save()

#             messages.success(request, "Staff Updated Successfully.")
#             return redirect('/edit_staff/'+staff_id)

#         except:
#             messages.error(request, "Failed to Update Staff.")
#             return redirect('/edit_staff/'+staff_id)


# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def delete_staff(request, staff_id):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     staff = Doctors.objects.get(admin=staff_id)
#     try:
#         staff.delete()
#         messages.success(request, "Staff Deleted Successfully.")
#         return redirect('manage_staff')
#     except:
#         messages.error(request, "Failed to Delete Staff.")
#         return redirect('manage_staff')



# @csrf_exempt
# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def check_email_exist(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     email = request.POST.get("email")
#     user_obj = Customer.objects.filter(email=email).exists()
#     if user_obj:
#         return HttpResponse(True)
#     else:
#         return HttpResponse(False)


# @csrf_exempt
# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def check_username_exist(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     username = request.POST.get("username")
#     user_obj = Customer.objects.filter(username=username).exists()
#     if user_obj:
#         return HttpResponse(True)
#     else:
#         return HttpResponse(False)


# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def users_feedback_message(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     feedbacks = FeedBackStudent.objects.all()
#     context = {
#         "feedbacks": feedbacks
#     }
#     return render(request, 'hod_template/users_feedback_template.html', context)


# @csrf_exempt
# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def users_feedback_message_reply(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     feedback_id = request.POST.get('id')
#     feedback_reply = request.POST.get('reply')

#     try:
#         feedback = FeedBackUser.objects.get(id=feedback_id)
#         feedback.feedback_reply = feedback_reply
#         feedback.save()
#         return HttpResponse("True")

#     except:
#         return HttpResponse("False")

# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def staff_feedback_message(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     feedbacks = FeedBackDoctors.objects.all()
#     context = {
#         "feedbacks": feedbacks
#     }
#     return render(request, 'hod_template/staff_feedback_template.html', context)


# @csrf_exempt
# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def staff_feedback_message_reply(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     feedback_id = request.POST.get('id')
#     feedback_reply = request.POST.get('reply')

#     try:
#         feedback = FeedBackDoctors.objects.get(id=feedback_id)
#         feedback.feedback_reply = feedback_reply
#         feedback.save()
#         return HttpResponse("True")

#     except:
#         return HttpResponse("False")




# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def staff_leave_view(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     leaves = LeaveReportStaff.objects.all()
#     context = {
#         "leaves": leaves
#     }
#     return render(request, 'hod_template/staff_leave_view.html', context)

# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def staff_leave_approve(request, leave_id):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     leave = LeaveReportDoctors.objects.get(id=leave_id)
#     leave.leave_status = 1
#     leave.save()
#     return redirect('staff_leave_view')

# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def staff_leave_reject(request, leave_id):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     leave = LeaveReportDoctors.objects.get(id=leave_id)
#     leave.leave_status = 2
#     leave.save()
#     return redirect('staff_leave_view')


# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def admin_profile(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     user = Customer.objects.get(id=request.user.id)

#     context={
#         "user": user
#     }
#     return render(request, 'hod_template/admin_profile.html', context)

# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# @login_required(login_url='login')
# def admin_profile_update(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     if request.method != "POST":
#         messages.error(request, "Invalid Method!")
#         return redirect('admin_profile')
#     else:
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         password = request.POST.get('password')

#         try:
#             customuser = Customer.objects.get(id=request.user.id)
#             customuser.first_name = first_name
#             customuser.last_name = last_name
#             if password != None and password != "":
#                 customuser.set_password(password)
#             customuser.save()
#             messages.success(request, "Profile Updated Successfully")
#             return redirect('admin_profile')
#         except:
#             messages.error(request, "Failed to Update Profile")
#             return redirect('admin_profile')
    

# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# def staff_profile(request):
#     admin_home = AdminHOD.objects.get(admin=request.user.id)
#     pass

# @cache_control(no_data=True, must_revalidade=True, no_strore=True)
# def student_profile(requtest):
    
    
#     pass