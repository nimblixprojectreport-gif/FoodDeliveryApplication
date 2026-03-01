from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):

    def validate(self, data):
        order = data['order']

        # ✅ Prevent duplicate payment for same order
        if Payment.objects.filter(order=order).exists():
            raise serializers.ValidationError("Payment already exists for this order")

        # ✅ Ensure correct amount
        if data['amount'] != order.total_amount:
            raise serializers.ValidationError("Incorrect payment amount")

        return data

    class Meta:
        model = Payment
        fields = '__all__'
