from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'mobile', 'password', 'role']

    def create(self, validated_data):
        mobile = validated_data.pop('mobile')
        user = User(**validated_data)
        user.phone_number = mobile
        user.set_password(validated_data['password'])
        user.save()
        return user


from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(phone_number=data['mobile']).first()
        if user and user.check_password(data['password']):
            return user
        raise serializers.ValidationError("Invalid credentials")
