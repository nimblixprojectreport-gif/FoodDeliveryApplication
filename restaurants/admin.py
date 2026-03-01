from django.contrib import admin
from .models import Restaurant, Menu, MenuItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('name', 'user__username')
    list_editable = ('is_approved',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'updated_at')
    inlines = [MenuItemInline]

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'price', 'is_veg', 'is_available')
    list_filter = ('is_veg', 'is_available')
    search_fields = ('name',)
