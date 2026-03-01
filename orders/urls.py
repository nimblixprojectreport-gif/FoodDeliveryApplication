from django.urls import path
from .views import (
    CartView,
    CheckoutView,
    OrderListView,
    OrderUpdateView,
    CartItemDeleteView,
    CancelOrderView,
    RestaurantOrdersView,   # ✅ NEW
)

urlpatterns = [
    path('', OrderListView.as_view()),                          # customer orders
    path('restaurant-orders/', RestaurantOrdersView.as_view()), # ✅ restaurant owner orders
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/<int:id>/', CartItemDeleteView.as_view()),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-orders/', OrderListView.as_view(), name='my-orders'),
    path('<int:id>/cancel/', CancelOrderView.as_view()),
    path('<int:id>/update-status/', OrderUpdateView.as_view(), name='update-order-status'),
]
