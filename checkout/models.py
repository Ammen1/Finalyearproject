from django.db import models
from django.utils.translation import gettext_lazy as _


class ServiceOptions(models.Model):
    """
    The Delivery methods table contining all delivery
    """

    SERVICE_CHOICES = [
        ("IS", "In Home"),
        ("HD", "Online"),
        ("DD", "Phone"),
    ]

    service_name = models.CharField(
        verbose_name=_("delivery_name"),
        help_text=_("Required"),
        max_length=255,
    )
    service_price = models.DecimalField(
        verbose_name=_("service price"),
        help_text=_("Maximum 9999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 9999.99."),
            },
        },
        max_digits=6,
        decimal_places=2,
    )
    service_method = models.CharField(
        choices=SERVICE_CHOICES,
        verbose_name=_("service_method"),
        help_text=_("Required"),
        max_length=255,
    )
    service_timeframe = models.CharField(
        verbose_name=_("serrvice timeframe"),
        help_text=_("Required"),
        max_length=255,
    )
    service_window = models.CharField(
        verbose_name=_("service window"),
        help_text=_("Required"),
        max_length=255,
    )
    order = models.IntegerField(verbose_name=_("list order"), help_text=_("Required"), default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Service Option")
        verbose_name_plural = _("Service Options")

    def __str__(self):
        return self.service_name


class PaymentSelections(models.Model):
    """
    services payment options
    """

    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("Required"),
        max_length=255,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Payment Selection")
        verbose_name_plural = _("Payment Selections")

    def __str__(self):
        return self.name

