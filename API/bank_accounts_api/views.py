from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from bank_accounts_api.models import Operation, Card
from bank_accounts_api.serializers import OperationsSerializer, ShowOperationsSerializer
from rest_framework import status

class OperationsApiView(APIView):

    def get(self,request,pk_card,pk=None):
        if pk==None:
            cards=request.user.cards.filter(id=pk_card).first()
            operations = cards.get_all_operations()
            for operation in operations:
                if operation.sender_card.id==pk_card:
                    operation.egreso=True
                else:
                    operation.egreso=False
            operations_serializer=ShowOperationsSerializer(operations,many=True)
            return Response(operations_serializer.data, status.HTTP_200_OK)
        else:
            cards=request.user.cards.filter(id=pk_card).first()
            operation = cards.get_all_operations().filter(id=pk).first()
            if operation==None:
                return Response({"error_messages":["No existe la operación solicitada"]}, status.HTTP_404_NOT_FOUND)
            if operation.sender_card.id==pk_card:
                operation.egreso=True
            else:
                operation.egreso=False
            operations_serializer=ShowOperationsSerializer(operation)
            return Response(operations_serializer.data, status.HTTP_200_OK)
    
    def post(self,request,pk_card):
        card = request.user.cards.get(id=pk_card)
        data=request.data
 
        if int(data["pin"]) == int(card.decrypt_pin(data["pin"])):
            account_number_destinity=data["account_number"]
            card_origin=card
            card_destinity=Card.objects.get(account_number=account_number_destinity)
            sufficient_balance = float(card_origin.get_balance())>=float(data["amount"])
            data["sender_card"]=card_origin.id
            data["receiving_card"]=card_destinity.id
            data["egreso"]=True
            operation_serializer=OperationsSerializer(data=data)
            diferentes_cuentas = card_origin.id!=card_destinity.id
            print(f'\n\n\n{operation_serializer.is_valid()}{sufficient_balance}{diferentes_cuentas}\n\n\n')
            if  operation_serializer.is_valid() and sufficient_balance and diferentes_cuentas:
                operation_serializer.save()
                return Response(operation_serializer.data,status.HTTP_200_OK)
            if not sufficient_balance:
                return Response({"error_messages":["Saldo insuficiente"]},status.HTTP_403_FORBIDDEN)
            if not diferentes_cuentas:
                return Response({"error_messages":["Saldo insuficiente"]},status.HTTP_403_FORBIDDEN)
            return Response(operation_serializer.errors,status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error":"Pin incorrecto"},status.HTTP_403_FORBIDDEN)
        
"""
origin_data=request.data.copy()
            origin_data["card"]=card_origin.id
            origin_data["egreso"]=True
            destinity_data=request.data
            destinity_data["card"]=card_destinity.id
            destinity_data["egreso"]=False
            operation_origin=OperationsSerializer(data=origin_data)
            operation_destinity=OperationsSerializer(data=destinity_data)
            print(f"datos origen{origin_data}")
            print(f"datos destino{destinity_data}")
"""