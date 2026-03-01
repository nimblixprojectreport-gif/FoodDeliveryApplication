import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')
django.setup()

from django.contrib.auth import get_user_model
from restaurants.models import Restaurant, Menu, MenuItem
from delivery.models import DeliveryProfile

User = get_user_model()

def create_users():
    # Create Restaurant User
    rest_user, created = User.objects.get_or_create(username='pizza_palace', email='pizza@example.com', role='RESTAURANT')
    if created:
        rest_user.set_password('password123')
        rest_user.save()
        restaurant = Restaurant.objects.create(user=rest_user, name='Pizza Palace', address='123 Pizza St', contact_number='1234567890', is_approved=True)
        menu = Menu.objects.create(restaurant=restaurant)
        MenuItem.objects.create(menu=menu, name='Margherita Pizza', description='Cheese and Tomato', price=12.99, is_veg=True)
        MenuItem.objects.create(menu=menu, name='Pepperoni Pizza', description='Pepperoni and Cheese', price=14.99, is_veg=False)
        print("Created Restaurant: Pizza Palace")

    # Create Delivery Custom User
    del_user, created = User.objects.get_or_create(username='delivery_dave', email='dave@example.com', role='DELIVERY')
    if created:
        del_user.set_password('password123')
        del_user.save()
        DeliveryProfile.objects.create(user=del_user, current_location='Downtown')
        print("Created Delivery Partner: Delivery Dave")

    # Create Customer User
    cust_user, created = User.objects.get_or_create(username='hungry_customer', email='customer@example.com', role='CUSTOMER')
    if created:
        cust_user.set_password('password123')
        cust_user.save()
        print("Created Customer: Hungry Customer")

if __name__ == '__main__':
    create_users()
