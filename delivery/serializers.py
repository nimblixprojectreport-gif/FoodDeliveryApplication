from rest_framework import serializers
from .models import DeliveryProfile, Delivery
from orders.serializers import OrderSerializer

class DeliveryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryProfile
        fields = '__all__'
        read_only_fields = ['user', 'joined_at']

    def validate(self, data):
        vehicle_type = data.get('vehicle_type')
        license_number = data.get('license_number')

        if not vehicle_type:
            raise serializers.ValidationError({"vehicle_type": "Vehicle type is required."})

        if not license_number:
            raise serializers.ValidationError({"license_number": "License number is required."})

        return data

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'