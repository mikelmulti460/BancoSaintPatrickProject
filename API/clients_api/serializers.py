from rest_framework import serializers
from . import models
from bank_accounts_api.serializers import ClientCardSerializer

class UserClientSerializer(serializers.ModelSerializer):
    """Serializador para un usuario tipo cliente"""
    cards = ClientCardSerializer(read_only=True,many=True)
    class Meta:
        model = models.UserClient
        fields = ('id', 'email', 'name', 'last_name', 'password', 'pin', 'cards',)
        extra_kwargs = {
            'password': {
                'write_only':True,
                'style': {'input_type':'password'}
            },
            'pin':{
                'write_only': True,
                'style':{'input_type':'password'}
            },
        }

    def create(self, validated_data):
        user = models.UserClient.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            last_name = validated_data['last_name'],
            password = validated_data['password'],
            pin = validated_data['pin']
        )
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)