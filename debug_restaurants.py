import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')
django.setup()

from restaurants.models import Restaurant, Menu

print(f"{'Rest ID':<10} {'Name':<20} {'Menu Exists'}")
print("-" * 40)
for rest in Restaurant.objects.all():
    has_menu = hasattr(rest, 'menu')
    print(f"{rest.id:<10} {rest.name:<20} {has_menu}")
