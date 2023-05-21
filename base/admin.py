from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django import forms

# Register your models here.

from .models import Doctors,Appointment,Category, Country,Hospital,Review,FeedBackUser,FeedBackDoctors,NotificationUsers,NotificationDoctors,HospitalImage,HospitalType,LeaveReportDoctors, HospitalSpecification



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
        ("general", {"fields": ("name","diagnostic_equipment","location","latitude","longitude","monitoring_sife_support_equipment","surgical_equipment","patient_care_equipment","emergency_trauma_equipmen","pharmacy_medication_management","support_services","accreditations_certifications","doctor_information","patient_resources","wait_times","insurance_payment_options","phone_number","hospital_beds","slug","title","hospital_profiles","specialties_services")}),
        ("other", {"fields": ("is_active",)}),
    )
    inlines = (HospitalImageInline,)

    # Order the sections within the change form
    jazzmin_section_order = ("hospital name", "category", "other")














