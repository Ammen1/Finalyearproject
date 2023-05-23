from django.db import models
from django.contrib.auth.models import AbstractUser
from account.models import Customer
from django.db.models.signals import post_save
from django.dispatch import receiver
import geocoder
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.text import slugify
from geopy.geocoders import Nominatim
from django.core.exceptions import ValidationError


class Category(MPTTModel):
    """
    Category Table implimented with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("base:category_list", args=[self.slug])

    def __str__(self):
        return self.name



class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



# class Country(models.Model):
#     """
#     Address
#     """
#     Hospital = models.ForeignKey("Hospital", verbose_name=_("category"),help_text=_("Not_required"), on_delete=models.CASCADE, blank=True)
#     state = models.CharField(max_length=100, null=True)
#     latitude = models.FloatField(default=0)
#     longitude = models.FloatField(default=0)
#     slug = models.SlugField(max_length=255, unique=True)
#     is_active = models.BooleanField(
#         verbose_name=_("Country visibility"),
#         help_text=_("Change country visibility"),
#         default=True,
#     )

#     class Meta:
#         verbose_name_plural = 'Data'

#     def save(self, *args, **kwargs):
#         self.latitude = geocoder.osm(self.country).lat
#         self.longitude = geocoder.osm(self.country).lng
#         return super().save(*args, **kwargs)

#     def get_absolute_url(self):
#         return reverse("base:hospital_detail", args=[self.slug])

#     def __str__(self):
#         return self.state
        
class Country(models.Model):
    """
    Address
    """
    state = models.CharField(max_length=100, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(
        verbose_name=_("Country visibility"),
        help_text=_("Change country visibility"),
        default=True,
    )

    class Meta:
        verbose_name_plural = 'Data'

    def save(self, *args, **kwargs):
        self.latitude = geocoder.osm(self.state).lat
        self.longitude = geocoder.osm(self.state).lng
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("base:hospital_detail", args=[self.slug])

    def __str__(self):
        return self.state


class HospitalType(models.Model):
    """
    HospitalType Table will provide a list of the different types
    of products that are for sale.
    """

    name = models.CharField(verbose_name=_("Hospital Name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("HospitalType")
        verbose_name_plural = _("HospitalType")

    def __str__(self):
        return self.name



class HospitalSpecification(models.Model):
    """
    The Hospital Specification Table contains hospital
    specifiction or features for the hospital types.
    """

    Hospital_type = models.ForeignKey(HospitalType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name



class Hospital(models.Model):
    """
    The Hospital table contining all product items.
    """
    location = models.CharField(max_length=100, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    name = models.CharField(verbose_name=_("name"), help_text=_("Required"), max_length=255)
    equiments = models.TextField(verbose_name=_("equiments"),)
    accreditations_certifications= models.CharField(verbose_name=_("accreditations_certifications"),help_text=_("Not Required"), blank=True,max_length=255)
    doctor_information= models.CharField(verbose_name=_("doctor_information"),help_text=_("Not Required"), blank=True,max_length=255)
    insurance_payment_options= models.CharField(verbose_name=_("insurance_payment_options"),help_text=_("Not Required"), blank=True,max_length=255)
    phone_number = models.CharField(verbose_name=_("phone_number"), max_length=20)
    hospital_beds = models.IntegerField(verbose_name=_("hospital_beds"),default=0)
    website = models.URLField(verbose_name=_("website"))
    title = models.CharField(verbose_name=_("title"),help_text=_("Required For Hospital Profile"),max_length=255)
    hospital_profiles = models.TextField(verbose_name=_("hospital_profiles"), help_text=_("Not Required"), blank=True)
    specialties_services = models.TextField(verbose_name=_("disease_treatment"),)
    slug = models.SlugField(verbose_name=_("slug"),max_length=255)
    is_active = models.BooleanField(verbose_name=_("Hospital visibility"),help_text=_("Change hospital visibility"),default=True,)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Hospital")
        verbose_name_plural = _("Hospitals")

    def clean(self):
        # Custom model-level validation logic
        if any(char.isdigit() for char in self.name):
            raise ValidationError(_("Name must not contain numbers."))


    def save(self, *args, **kwargs):
        self.latitude = geocoder.osm(self.location).lat
        self.longitude = geocoder.osm(self.location).lng
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("base:hospital_detail", args=[self.slug])   

    def __str__(self):
        return f"{self.name}, {self.title}"



class HospitalSpecificationValue(models.Model):
    """
    The Hospital Specification Value table holds each of the
    hospitals individual specification or bespoke features.
    """

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    specification = models.ForeignKey(HospitalSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Hospital specification value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Hospital Specification Value")
        verbose_name_plural = _("Hospital Specification Values")

    def __str__(self):
        return self.value




class HospitalImage(models.Model):
    """
    The Hospital Image table.
    """

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="hospital_image")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a hospital image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Hospital Image")
        verbose_name_plural = _("Hospital Images")

  

class Review(models.Model):
    user = models.ForeignKey(Customer, on_delete = models.CASCADE, null=True)
    hospital = models.ForeignKey(Hospital, on_delete = models.CASCADE, null=True) 
    comment = models.TextField(max_length=250)
    rate  = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id







class FeedBackUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Feedback with {self.user_id.name} on {self.user_id.id}"


class MessageUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    message_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Chat with {self.user_id.name} on {self.user_id.id}"



class NotificationUsers(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()





class Doctors(models.Model):
    admin = models.OneToOneField(Customer, on_delete=models.CASCADE)
    role = models.CharField(_("Role"), help_text=_("Required"), max_length=100)
    gender = models.CharField(max_length=1)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)
    specialization = models.CharField(verbose_name=_("Specialization"), help_text=_("Required"), max_length=255)
    bio = models.TextField(verbose_name=_("Biography"), help_text=_("Enter doctor's biography"), null=True, blank=True)
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a hospital image"),
        upload_to="images/",
        default="images/default.png",
    )
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(help_text=_("Change Doctor visibility"),default=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_("Doctor visibility"),
        help_text=_("Change Doctor visibility"),
        default=False,
    )
 

    class Meta:
        verbose_name_plural = 'Doctors'

    def clean(self):
        # Custom model-level validation logic
        if any(char.isdigit() for char in self.name):
            raise ValidationError(_("Name must not contain numbers."))

    def get_absolute_url(self):
        return reverse("appointment:doctor_detail", args=[self.slug])

    def __str__(self):
        return self.name



class Appointment(models.Model):
    admin = models.OneToOneField(Customer, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    country = models.CharField(verbose_name=_("name"), help_text=_("Required"), max_length=100, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(
        verbose_name=_("doctor visibility"),
        help_text=_("Change doctor visibility"),
        default=True,
    )

    class Meta:
        verbose_name_plural = 'appointments'

    def save(self, *args, **kwargs):
        self.latitude = geocoder.osm(self.country).lat
        self.longitude = geocoder.osm(self.country).lng
        return super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("appointment:doctor_detail", args=[self.slug])

    

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.appointment_date}"


class LeaveReportDoctors(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()        



class FeedBackDoctors(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()  

    def __str__(self):
        return f"Feedback with {self.staff_id.name} on {self.staff_id.id}"

class NotificationDoctors(models.Model):
    id = models.AutoField(primary_key=True)
    doctor_id = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
