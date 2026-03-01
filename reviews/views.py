from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import ReviewSerializer
from orders.models import Order

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        order_id = request.data.get('order_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')

        if not order_id:
            return Response({"error": "order_id required"}, status=400)

        order = get_object_or_404(Order, id=order_id, customer=request.user)

        # Business Rule: Only delivered orders can be reviewed
        if order.status != 'DELIVERED':
            return Response(
                {"error": "Only delivered orders can be reviewed"},
                status=400
            )

        # Prevent duplicate reviews
        if hasattr(order, 'review'):
            return Response(
                {"error": "Order already reviewed"},
                status=400
            )

        review = Review.objects.create(
            customer=request.user,
            order=order,
            restaurant=order.restaurant,
            rating=rating,
            comment=comment
        )

        return Response(ReviewSerializer(review).data, status=201)
