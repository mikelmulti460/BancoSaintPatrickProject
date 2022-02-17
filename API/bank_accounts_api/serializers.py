from dataclasses import field
from rest_framework import serializers
from bank_accounts_api.models import Card, Operation

class ClientCardSerializer(serializers.ModelSerializer):
    class Meta:
        model=Card
        fields = ('id','account_number','last_digits')
    
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model=Card
        fields = ("card_number","expiration_date","ccv")

class OperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Operation
        fields = "__all__"

class ShowOperationsSerializer(serializers.ModelSerializer):
    receiving_card=serializers.StringRelatedField()
    sender_card=serializers.StringRelatedField()
    class Meta:
        model=Operation
        fields = ("__all__")