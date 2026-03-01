from django.urls import path
from .views import (
    DeliveryStatusView,
    AvailableOrdersView,
    AcceptOrderView,
    UpdateDeliveryStatusView,
)

urlpatterns = [
    # GET  → my assigned orders (history)
    # POST → update availability / location
    path('status/', DeliveryStatusView.as_view(), name='delivery-status'),

    # GET  → available orders to accept (PREPARING, no partner)
    path('orders/available/', AvailableOrdersView.as_view(), name='available-orders'),

    # POST → accept an order
    path('orders/<int:order_id>/accept/', AcceptOrderView.as_view(), name='accept-order'),

    # POST → update status { status: PICKED_UP | OUT_FOR_DELIVERY | DELIVERED }
    path('orders/<int:order_id>/update-status/', UpdateDeliveryStatusView.as_view(), name='update-delivery-status'),
]
