from rest_framework import serializers
from .models import Detail, User

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'imei', 'user_name', 'car_owner',
            'license_number', 'vin', 'is_tracking'
        )
