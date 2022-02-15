from rest_framework import serializers
from . import models

class ClientCardSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Card
        fields = ('id','account_number','last_digits')
    
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Card
        fields = ("card_number","expiration_date","ccv")