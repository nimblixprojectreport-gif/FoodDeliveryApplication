from django.contrib import admin
from .models import Delivery, DeliveryProfile

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_partner', 'status', 'assigned_at')
    list_filter = ('status',)
    search_fields = ('order__id',)

@admin.register(DeliveryProfile)
class DeliveryProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_available', 'current_location', 'joined_at')
