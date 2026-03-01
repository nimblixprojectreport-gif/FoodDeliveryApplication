from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from .models import Restaurant, Menu, MenuItem
from .serializers import RestaurantSerializer, CreateRestaurantSerializer, MenuSerializer, CreateMenuItemSerializer, MenuItemSerializer
from django.shortcuts import get_object_or_404

class IsRestaurantOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'RESTAURANT'

class RestaurantCreateView(generics.CreateAPIView):
    serializer_class = CreateRestaurantSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def perform_create(self, serializer):
        restaurant = serializer.save(user=self.request.user, is_approved=True)
        Menu.objects.create(restaurant=restaurant)

class RestaurantDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get_object(self):
        return get_object_or_404(Restaurant, user=self.request.user)

class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.filter(is_approved=True)
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]

class MenuDetailView(generics.RetrieveAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return get_object_or_404(Menu, restaurant_id=restaurant_id)

class MenuItemCreateView(generics.CreateAPIView):
    serializer_class = CreateMenuItemSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, user=self.request.user)
        menu, created = Menu.objects.get_or_create(restaurant=restaurant)
        serializer.save(menu=menu)

class MenuItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateMenuItemSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]
    lookup_field = 'id'

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, user=self.request.user)
        menu = get_object_or_404(Menu, restaurant=restaurant)
        return MenuItem.objects.filter(menu=menu)
    
class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]


class PublicRestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.filter(is_approved=True)
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"