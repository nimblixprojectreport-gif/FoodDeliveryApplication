from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, PlaceOrderSerializer
from restaurants.models import MenuItem, Restaurant
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import RetrieveAPIView


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Skip CSRF check


TOKEN_AUTH = [TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication]


class CartView(APIView):
    authentication_classes = TOKEN_AUTH
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        menu_item_id = request.data.get('menu_item_id')
        quantity = int(request.data.get('quantity', 1))

        menu_item = get_object_or_404(MenuItem, id=menu_item_id)

        if cart.items.exists():
            existing_restaurant = cart.items.first().menu_item.menu.restaurant
            if existing_restaurant != menu_item.menu.restaurant:
                return Response(
                    {'error': 'Cannot add items from different restaurants. Clear your cart first.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response(CartSerializer(cart).data)

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'})


class CheckoutView(APIView):
    authentication_classes = TOKEN_AUTH
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        restaurant = cart.items.first().menu_item.menu.restaurant
        total_amount = cart.total_price()

        order = Order.objects.create(
            customer=request.user,
            restaurant=restaurant,
            total_amount=total_amount,
            delivery_address=request.data.get('delivery_address', 'Default Address')
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                menu_item_name=item.menu_item.name,
                quantity=item.quantity,
                price=item.menu_item.price
            )

        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


# ✅ Customer: see own orders
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = TOKEN_AUTH

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-created_at')


# ✅ NEW: Restaurant owner sees orders placed at their restaurant
class RestaurantOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = TOKEN_AUTH

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, user=self.request.user)
        return Order.objects.filter(restaurant=restaurant).order_by('-created_at')


class OrderUpdateView(APIView):
    authentication_classes = TOKEN_AUTH
    permission_classes = [permissions.IsAuthenticated]

    VALID_STATUSES = ['PENDING', 'PREPARING', 'PICKED_UP', 'OUT_FOR_DELIVERY', 'DELIVERED', 'CANCELLED']

    def put(self, request, id):
        order = get_object_or_404(Order, id=id)
        new_status = request.data.get('status')
        if not new_status:
            return Response({'error': 'status field is required'}, status=status.HTTP_400_BAD_REQUEST)
        if new_status not in self.VALID_STATUSES:
            return Response({'error': f'Invalid status. Choose from: {", ".join(self.VALID_STATUSES)}'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)

    def patch(self, request, id):
        return self.put(request, id)


class CartItemDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = TOKEN_AUTH

    def delete(self, request, id):
        cart_item = get_object_or_404(CartItem, id=id, cart__user=request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CancelOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = TOKEN_AUTH

    def post(self, request, id):
        order = get_object_or_404(Order, id=id, customer=request.user)

        if order.status != "PENDING":
            return Response({"error": "Only pending orders can be cancelled"}, status=400)

        order.status = "CANCELLED"
        order.save()

        return Response({"message": "Order cancelled"})


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = TOKEN_AUTH
    lookup_field = 'id'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
