from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from base.EmailBackEnd import EmailBackEnd
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage 
from django.shortcuts import render
from .models import Doctors,LeaveReportDoctors,MessageUser, Country,Hospital,FeedBackUser,FeedBackDoctors,Appointment
import folium
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from folium import plugins
from django.views.decorators.cache import cache_control
import json
import requests
from math import radians, sin, cos, sqrt, atan2
from account.models import Customer
from geopy import distance
from geopy.distance import geodesic
from django.http import JsonResponse

def submit_rating(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        # Perform any validation or processing of the rating value here

        # Update the hospital_rating in your Django model accordingly
        # Assuming you have a Hospital model with a hospital_rating field
        hospital = Hospital.objects.get(pk=request.hospital)  # Replace 1 with the actual hospital record you want to update
        hospital.hospital_rating = rating
        hospital.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})






def index(request):
    url = ("https://raw.githubusercontent.com/python-visualization/folium/main/examples/data")
    vis1 = json.loads(requests.get(f"{url}/vis1.json").text)
    vis2 = json.loads(requests.get(f"{url}/vis2.json").text)
    vis3 = json.loads(requests.get(f"{url}/vis3.json").text)
    data = Country.objects.all()
    data_list = Country.objects.values_list('latitude', 'longitude')

    map1 = folium.Map(location=[10.2116702, 38.6521203],
                      tiles='CartoDB Dark_Matter', zoom_start=8)
    tooltip = "Click me!"
    folium.Marker([10.2116702, 38.6521203], popup="<i>{{ country }}</i>", tooltip=tooltip).add_to(map1)
 
    map1 = folium.Map(location=[8.5410261, 39.2705461], zoom_start=7, tiles="Stamen Terrain")

    folium.Marker(location=[9.0107934, 38.7612525],popup=folium.Popup(max_width=450).add_child(folium.Vega(vis1, width=450, height=250)),).add_to(map1)

    folium.Marker(location=[8.286087, 37.781844],popup=folium.Popup(max_width=450).add_child(folium.Vega(vis2, width=450, height=250)),).add_to(map1)

    folium.Marker(location=[7.2116702, 40.6521203],popup=folium.Popup(max_width=450).add_child(folium.Vega(vis3, width=450, height=250)),).add_to(map1)
    #define the two points
    # point1 = (9.0107934, 38.7612525) # Portland, OR
    # point2 = (8.5410261, 39.2705461) # Seattle, WA
    # # calculate the distance between the points using the Haversine formula
    # R = 6373.0 # approximate radius of earth in km
    # lat1 = radians(point1[0])
    # lon1 = radians(point1[1])
    # lat2 = radians(point2[0])
    # lon2 = radians(point2[1])
    
    # dlon = lon2 - lon1
    # dlat = lat2 - lat1
    # a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    # c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # distance = R * c
    # # create a Folium map and add markers for the two points
    # map1 = folium.Map(location=[point1[0], point1[1]], zoom_start=6)
    # folium.Marker(location=[point1[0], point1[1]], popup='Point 1').add_to(map1)
    # folium.Marker(location=[point2[0], point2[1]], popup='Point 2').add_to(map1)
    #  # add a popup with the distance between the points
    # folium.Popup(f'Distance between points: {distance:.2f} km').add_to(folium.PolyLine(locations=[point1, point2]))


    plugins.HeatMap(data_list).add_to(map1)
    plugins.Fullscreen(position='topright').add_to(map1)
    map1 = map1._repr_html_()
    context = {
        'map1': map1
    }
    return render(request, 'store/map.html', context)





def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    hospitals = Hospital.objects.filter(
        category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
    )
    return render(request, "store/category.html", {"category": category, "hospitals": hospitals})

def hospital_all(request):
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(name__icontains=q)| Q(title__icontains=q) | Q(specialties_services__icontains=q) | Q(location__icontains=q)| Q(equiments__icontains=q))
        hospitals = Hospital.objects.prefetch_related("hospital_image").filter(multiple_q, is_active=True)
    else:
        hospitals = Hospital.objects.prefetch_related("hospital_image").filter(is_active=True)
    doctors = Doctors.objects.all()
    hospital_count = hospitals.count()
    context = {"hospitals": hospitals, 'hospital_count':hospital_count,'doctors':doctors}
    return render(request, "store/index.html", context)


def calculate_distance(point1, point2):
    return geodesic(point1, point2).kilometers



def hospital_detail(request, slug):
    hospital = get_object_or_404(Hospital, slug=slug, is_active=True)
    # Define the reference location
    ref_location = (7.6792877, 36.853324750435384)
    hospitals = Hospital.objects.all()
    hospital_rating = 4.8

    query = request.GET.get('q')  # Get the search query from the request

    if query:
        hospitals = search_hospitals(query)
    # Calculate the distance from the reference location to the hospital location
    hospital_location = (hospital.latitude, hospital.longitude)
    distance_to_hospital = calculate_distance(ref_location, hospital_location)

    # Create a folium map for the hospital location
    hospital_map = folium.Map(location=hospital_location, zoom_start=7)
    folium.Marker(location=hospital_location, popup=hospital.location).add_to(hospital_map)

    # Add the distance from the reference location to the hospital location as a popup message
    popup_message = f"Distance from reference location: {distance_to_hospital:.2f} km"
    folium.Marker(location=ref_location, popup=popup_message, icon=folium.Icon(color='red')).add_to(hospital_map)

    # Generate the HTML code for the map
    map_html = hospital_map._repr_html_()
    #search
    
    
    


    # Pass the folium maps to the template
    context = {"hospital": hospital, 'map_html': map_html,'query': query,'hospital_rating': hospital_rating}
    return render(request, "store/single.html", context)





# def map(request,slug):
#     hospital = get_object_or_404(Country, slug=slug, is_active=True)
#     ref_location = (13.4966644, 39.4768259)

#     # Retrieve all hospitals from the database
    

#     # Create a folium map for each hospital
#     maps = []
#     for hospital in hospitals:
#         # Calculate the distance from the reference location to the hospital location
#         hospital_location = (hospital.latitude, hospital.longitude)
#         distance_to_hospital = calculate_distance(ref_location, hospital_location)

#         # Create a folium map for the hospital location
#         hospital_map = folium.Map(location=hospital_location, zoom_start=15)
#         folium.Marker(location=hospital_location, popup=hospital.country).add_to(hospital_map)

#         # Add the distance from the reference location to the hospital location as a popup message
#         popup_message = f"Distance from reference location: {distance_to_hospital:.2f} km"
#         folium.Marker(location=ref_location, popup=popup_message, icon=folium.Icon(color='red')).add_to(hospital_map)

#         maps.append(hospital_map._repr_html_())

#     # Generate the HTML code for the maps
#     maps_html = "".join(maps)

#     context = {'maps_html': maps_html}
#     return render(request, "store/single.html", context)


def submit_rating(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        # Perform any validation or processing of the rating value here

        # Update the hospital_rating in your Django model accordingly
        # Assuming you have a Hospital model with a hospital_rating field
        hospital = Hospital.objects.get(pk=1)  # Replace 1 with the actual hospital record you want to update
        hospital.hospital_rating = rating
        hospital.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})




@csrf_exempt
def save_location(request):
    
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # save the user's location to the database or perform any other necessary actions

        return HttpResponse('Location saved successfully')



def doctor_list(request):
    doctors = Doctors.objects.all()
    return render(request, 'store/doctor_list.html', {'doctors': doctors})

def doctor_detail(request, slug):
    doctor = get_object_or_404(Doctors, slug=slug)
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'store/doctor_detail.html', {'doctor': doctor, 'appointments': appointments})







def home(request):
    # hospitals = Hospital.objects.prefetch_related("hospital_image").filter(is_active=True)
    # hospital_count = hospitals.count()
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,"hospitals": hospitals,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)



@login_required
def staff_apply_leave(request):
    staff_obj = Doctors.objects.get(id=request.user.id, is_staff=True)
    leave_data = LeaveReportDoctors.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "account/dashboard/staff_apply_leave_template.html", context)

@login_required
def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('base:staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Doctors.objects.get(id=request.user.id)
        try:
            leave_report = LeaveReportDoctors(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('base:staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('base:staff_apply_leave')

@login_required
def staff_feedback(request):
    staff_obj = Doctors.objects.get(id=request.user.id,is_staff=True)
    feedback_data = FeedBackDoctors.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "account/dashboard/staff_feedback_template.html", context)

@login_required
def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('base:staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Doctors.objects.get(id=request.user.id)

        try:
            add_feedback = FeedBackDoctors(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('bass:staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('base:staff_feedback')


@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def users_feedback_message(request):
    admin_home = Customer.objects.get(id=request.user.id)
    feedbacks = FeedBackUser.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'account/dashboard/users_feedback_template.html', context)


@csrf_exempt
@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def users_feedback_message_reply(request):
    admin_home = Customer.objects.get(id=request.user.id,is_superuser=True)
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackUser.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def staff_feedback_message(request):
    admin_home = Customer.objects.get(id=request.user.id, is_superuser=True)
    feedbacks = FeedBackDoctors.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'account/dashboard/staff_feedback_templates.html', context)


@csrf_exempt
@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def staff_feedback_message_reply(request):
    admin_home = Customer.objects.get(id=request.user.id, is_superuser=True)
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackDoctors.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")




@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def staff_leave_view(request):
    admin_home = Customer.objects.get(id=request.user.id, is_superuser=True)
    leaves = LeaveReportDoctors.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'account/dashboard/staff_leave_view.html', context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def staff_leave_approve(request, leave_id):
    admin_home = Customer.objects.get(id=request.user.id, is_superuser=True)
    leave = LeaveReportDoctors.objects.get(id=leave_id)
    leave.leave_status = 1
    user.is_active = False
    leave.save()
    return redirect('base:staff_leave_view')

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def staff_leave_reject(request, leave_id):
    admin_home = Customer.objects.get(id=request.user.id, is_superuser=True)
    leave = LeaveReportDoctors.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('base:staff_leave_view')



@cache_control(no_data=True, must_revalidade=True, no_strore=True)
def users_feedback(request):
    student_obj = Customer.objects.get(id=request.user.id)
    feedback_data = FeedBackUser.objects.filter(user_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'account/dashboard/users_feedback.html', context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
def users_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('base:users_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Customer.objects.get(id=request.user.id)

        try:
            add_feedback = FeedBackUser(user_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('base:users_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('base:users_feedback')

def services(request):
    url = ("https://raw.githubusercontent.com/python-visualization/folium/main/examples/data")
    vis1 = json.loads(requests.get(f"{url}/vis1.json").text)
    vis2 = json.loads(requests.get(f"{url}/vis2.json").text)
    vis3 = json.loads(requests.get(f"{url}/vis3.json").text)
    data = Country.objects.all()
    data_list = Country.objects.values_list('latitude', 'longitude')

    map1 = folium.Map(location=[10.2116702, 38.6521203],
                      tiles='CartoDB Dark_Matter', zoom_start=8)
    tooltip = "Click me!"
    folium.Marker([10.2116702, 38.6521203], popup="<i>{{ country }}</i>", tooltip=tooltip).add_to(map1)
 
    map1 = folium.Map(location=[8.5410261, 39.2705461], zoom_start=7, tiles="Stamen Terrain")

    folium.Marker(location=[9.0107934, 38.7612525],popup=folium.Popup(max_width=450).add_child(folium.Vega(vis1, width=450, height=250)),).add_to(map1)

    folium.Marker(location=[8.286087, 37.781844],popup=folium.Popup(max_width=450).add_child(folium.Vega(vis2, width=450, height=250)),).add_to(map1)

    folium.Marker(location=[7.2116702, 40.6521203],popup=folium.Popup(max_width=450).add_child(folium.Vega(vis3, width=450, height=250)),).add_to(map1)
    plugins.HeatMap(data_list).add_to(map1)
    plugins.Fullscreen(position='topright').add_to(map1)
    map1 = map1._repr_html_()
    context = {
        'map1': map1
    }
   

    return render(request, 'store/service.html',context)


def about(request):
    return render(request, 'store/about.html')    


def contact(request):
    return render(request, 'store/contact.html')    







#privetchat

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
def users_message(request):
    student_obj = Customer.objects.get(id=request.user.id)
    feedback_data = MessageUser.objects.filter(user_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'account/dashboard/users_message.html', context)

@cache_control(no_data=True, must_revalidade=True, no_strore=True)
def users_message_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('base:users_message')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Customer.objects.get(id=request.user.id)

        try:
            add_feedback = MessageUser(user_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "message Sent.")
            return redirect('base:users_message')
        except:
            messages.error(request, "Failed to Send users_message.")
            return redirect('base:users_message')



@login_required(login_url='login')
def users_message_view(request):
    admin_home = Customer.objects.get(id=request.user.id,is_staff=True)
    feedbacks = MessageUser.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'account/dashboard/users_template_view.html', context)


@csrf_exempt
@cache_control(no_data=True, must_revalidade=True, no_strore=True)
@login_required(login_url='login')
def users_message_reply(request):
    admin_home = Customer.objects.get(id=request.user.id, is_staff=True)
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackDoctors.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")



# @csrf_exempt
# @login_required(login_url='login')
# def users_feedback_message_reply(request):
#     admin_home = Customer.objects.get(id=request.user.id,is_staff=True)
#     feedback_id = request.POST.get('id')
#     feedback_reply = request.POST.get('reply')

#     try:
#         feedback = FeedBackUser.objects.get(id=feedback_id)
#         feedback.feedback_reply = feedback_reply
#         feedback.save()
#         return HttpResponse("True")

#     except:
#         return HttpResponse("False")
