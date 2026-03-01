from django.db import models
from orders.models import Order
from django.conf import settings

class Delivery(models.Model):

    STATUS_CHOICES = (
        ('ASSIGNED', 'Assigned'),
        ('PICKED_UP', 'Picked Up'),
        ('ON_THE_WAY', 'On The Way'),
        ('DELIVERED', 'Delivered'),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery'
    )

    delivery_partner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ASSIGNED'
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order.id} - {self.status}"

class DeliveryProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)

    is_available = models.BooleanField(default=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle_type}"