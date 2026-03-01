from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from restaurants.serializers import MenuItemSerializer

class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menu_item_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.CharField()
    
    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'status', 'total_amount', 'delivery_address', 'created_at', 'items']
        read_only_fields = ['restaurant', 'total_amount', 'created_at']

class PlaceOrderSerializer(serializers.Serializer):
    delivery_address = serializers.CharField()
