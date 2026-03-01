from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from django.shortcuts import get_object_or_404
from .models import DeliveryProfile
from .serializers import DeliveryProfileSerializer
from orders.models import Order
from orders.serializers import OrderSerializer

# Accept Token, Session, or Basic auth
TOKEN_AUTH = [TokenAuthentication, SessionAuthentication, BasicAuthentication]


def get_or_create_profile(user):
    profile, _ = DeliveryProfile.objects.get_or_create(user=user)
    return profile


# ─── GET  → all orders assigned to me (active + history)
# ─── POST → update my availability/location (auto-creates profile)
class DeliveryStatusView(APIView):
    authentication_classes = TOKEN_AUTH
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(
            delivery_partner=request.user
        ).order_by('-created_at')
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        profile = get_or_create_profile(request.user)

        if 'is_available' in request.data:
            val = request.data['is_available']
            if isinstance(val, bool):
                profile.is_available = val
            else:
                profile.is_available = str(val).lower() in ('true', '1', 'yes')

        if 'current_location' in request.data:
            profile.current_location = request.data['current_location']

        profile.save()
        return Response(DeliveryProfileSerializer(profile).data)


# ─── GET → orders with PREPARING status and no delivery partner
class AvailableOrdersView(generics.ListAPIView):
    authentication_classes = TOKEN_AUTH
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        get_or_create_profile(self.request.user)
        return Order.objects.filter(
            status='PREPARING',
            delivery_partner__isnull=True
        ).order_by('-created_at')


# ─── POST → accept an order
class AcceptOrderView(APIView):
    authentication_classes = TOKEN_AUTH
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        profile = get_or_create_profile(request.user)

        if not profile.is_available:
            return Response(
                {'error': 'You are Offline. Go Online first to accept orders.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = get_object_or_404(
            Order, id=order_id, delivery_partner__isnull=True, status='PREPARING'
        )

        order.delivery_partner = request.user
        order.status = 'PICKED_UP'
        order.save()

        profile.is_available = False
        profile.save()

        return Response(OrderSerializer(order).data)


# ─── POST → update delivery status  PICKED_UP → OUT_FOR_DELIVERY → DELIVERED
class UpdateDeliveryStatusView(APIView):
    authentication_classes = TOKEN_AUTH
    permission_classes = [permissions.IsAuthenticated]

    ALLOWED = ['PICKED_UP', 'OUT_FOR_DELIVERY', 'DELIVERED']

    def post(self, request, order_id):
        order = get_object_or_404(
            Order, id=order_id, delivery_partner=request.user
        )

        new_status = request.data.get('status')
        if new_status not in self.ALLOWED:
            return Response(
                {'error': f'Status must be one of: {", ".join(self.ALLOWED)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        # Free up driver when delivered
        if new_status == 'DELIVERED':
            profile = get_or_create_profile(request.user)
            profile.is_available = True
            profile.save()

        return Response(OrderSerializer(order).data)
