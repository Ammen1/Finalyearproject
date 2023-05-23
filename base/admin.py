from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django import forms

# Register your models here.

from .models import Doctors,Appointment,Category, Country,Hospital,Review,FeedBackUser,FeedBackDoctors,NotificationUsers,NotificationDoctors,HospitalImage,HospitalType,LeaveReportDoctors, HospitalSpecification,MessageUser



admin.site.register(Doctors)
admin.site.register(Appointment)
admin.site.register(Country)
admin.site.register(Review)
admin.site.register(FeedBackUser)
admin.site.register(FeedBackDoctors)
admin.site.register(NotificationUsers)
admin.site.register(NotificationDoctors)
admin.site.register(Category)
admin.site.register(HospitalType)
admin.site.register(LeaveReportDoctors)
admin.site.register(MessageUser)
# admin.site.register(website)
# admin.site.register(HospitalSpecificationValue)

class HospitalImageInline(admin.TabularInline):
    model = HospitalImage
    extra = 1

# class HospitalTypeInline(admin.TabularInline):
#     model = Category
#     extra = 1



@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    resource_class = Hospital
    fieldsets = (
        ("general", {"fields": ("name","equiments","location","latitude","longitude","accreditations_certifications","doctor_information","insurance_payment_options","phone_number","hospital_beds","slug","title","hospital_profiles","specialties_services")}),
        ("other", {"fields": ("is_active",)}),
    )
    inlines = (HospitalImageInline,)

    # Order the sections within the change form
    jazzmin_section_order = ("hospital name", "category", "other")














