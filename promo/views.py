from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PromoCode
from .serializers import PromoValidateSerializer

class PromoValidateView(APIView):

    def post(self, request):
        serializer = PromoValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        code = serializer.validated_data['code']
        order_amount = serializer.validated_data['order_amount']

        try:
            promo = PromoCode.objects.get(code=code, is_active=True)
        except PromoCode.DoesNotExist:
            return Response({"error": "Invalid promo code"}, status=400)

        discount = (order_amount * promo.discount_percentage) / 100
        final_amount = order_amount - discount

        return Response({
            "valid": True,
            "discount": discount,
            "final_amount": final_amount
        })
