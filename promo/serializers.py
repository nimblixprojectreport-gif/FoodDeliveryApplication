from rest_framework import serializers
from .models import PromoCode

class PromoValidateSerializer(serializers.Serializer):
    code = serializers.CharField()
    order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
