from django.urls import path
from .views import (
    RestaurantCreateView,
    RestaurantDetailView,
    RestaurantListView,
    MenuDetailView,
    MenuItemCreateView,
    MenuItemUpdateDeleteView,
    PublicRestaurantDetailView
)

urlpatterns = [
    path('register/', RestaurantCreateView.as_view(), name='restaurant-register'),

    # ✅ Public list (OpenAPI /restaurants)
    path('', RestaurantListView.as_view(), name='restaurant-list'),

    # ✅ Public details (OpenAPI /restaurants/{id})
    path('<int:id>/', PublicRestaurantDetailView.as_view(), name='restaurant-detail'),

    # ✅ Owner manage (keep existing logic)
    path('manage/', RestaurantDetailView.as_view(), name='restaurant-manage'),

    # ✅ Menu endpoints
    path('<int:restaurant_id>/menu/', MenuDetailView.as_view(), name='restaurant-menu'),
    path('menu/items/add/', MenuItemCreateView.as_view(), name='menu-item-add'),
    path('menu/items/<int:id>/', MenuItemUpdateDeleteView.as_view(), name='menu-item-manage'),
    path('menu-items/', MenuItemCreateView.as_view(), name='menu-items'),


]
