from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAdminUser
from . import serializers, models, permissions
from bank_accounts_api.serializers import CardSerializer, ClientCardSerializer

class HelpApiView(APIView):
    """Class for help about API"""

    def get(self, request, format=None):
        """Retorna una lista de características del API"""
        views_defined = {
            "Módulos":{
                "api":{
                    "description": "Funciones generales de la api",
                    "Views":{
                        "Help":{
                            "description": "Retorna una lista de características del API",
                            "url": "api/help/",
                            "methods":{"get":"Retorna una lista de características del API",},
                            "acceso":"Usuarios logueados"
                        },
                    },
                },
                "clients":{
                    "description": "Retorna una lista de clientes",
                    "Views":{
                        "Clients":{
                            "ulr":"api/clients/",
                            "methods":{"get":"Retorna una lista de clientes","post":{"description":"Añade un nuevo cliente","campos":['id', 'email', 'name', 'last_name', 'password', 'pin']}},
                            "acceso":"SuperUser"
                        },
                        "Client":{
                            "ulr":"api/client/",
                            "methods":{"get":"Retorna el cliente logueado actualmente"},
                            "acceso":"Solo cliente logueado"
                        },
                    }
                    
                },
                
                "cards":{
                    "description": "Retorna la lista de tarjetas del cliente actualmente logueado",
                    "Views":{
                        "Cards":{
                            "ulr":"api/client/cards/",
                            "methods":{"get":"Retorna la lista de tarjetas del cliente actualmente logueado"},
                            "acceso":"Solo cliente logueado"
                        },
                        "Card":{
                            "ulr":"api/client/cards/<int:id>",
                            "methods":{
                                "get":"Retorna los datos de la tarjeta(id) del cliente",
                                "post":{
                                    "description":"obtiene los datos de la tarjeta desencriptados",
                                    "campos":{"pin":"integer_field"}
                                }
                            },
                            "acceso":"Solo cliente logueado"
                        }
                    },
                },
                
                "operations":{
                    "description": "crear operaciones bancarias en las tarjetas de los clientes",
                    "Views":{
                        "Operations":{
                            "ulr":"api/client/cards/<int:card>/operations/",
                            "methods":{
                                "get":"Retorna una lista de operaciones vinculadas a la tarjeta identificada en parámetro",
                                "post":{
                                    "description":"Envia una nueva operación",
                                    "campos":["description","amount","account_number","pin"]
                                },
                            },
                            "acceso":"Solo cliente logueado"
                        },
                        "Card":{
                            "ulr":"api/client/cards/<int:id>/operations/<int:id>/",
                            "methods":{"get":"Retorna los datos de la transacción pasada por parámetro"},
                            "acceso":"Solo cliente logueado"
                        }
                    },
                },

            }
        }

        return Response(views_defined)

class UserClientsApiView(viewsets.ModelViewSet):
    serializer_class = serializers.UserClientSerializer
    queryset = models.UserClient.objects.all()
    authentication_classers = (TokenAuthentication,)
    permission_classes = (permissions.IsOwnerAndReadOnly, IsAdminUser)

class UserClientApiView(APIView):

    def get(self, request):
        if request.user.id:
            user = request.user
            user_serializer=serializers.UserClientSerializer(user)
            return Response(user_serializer.data, status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_200_OK)

class UserLoginApiView(ObtainAuthToken):
    """ Crea tokens de autenticación de usuario """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class CardAPIView(APIView):
    def get(self,request,pk=None):
        if pk==None:
            cards = request.user.cards.all()
            card_serializer = ClientCardSerializer(cards,many=True)
            return Response(card_serializer.data,status.HTTP_200_OK)
        else:
            card = request.user.cards.filter(id=pk).first()
            card_serializer = ClientCardSerializer(card)
            data={}
            data.update(card_serializer.data)
            data["balance"]=card.get_balance()
            return Response(data,status.HTTP_200_OK)

    def post(self, request, pk):
        user = request.user
        card = user.cards.filter(id=pk).first()
        if int(request.data["pin"])==int(card.decrypt_pin()) and pk!=None:
            data = card.decrypt_data(request.data["pin"])
            card.card_number=data['card_number']
            card.ccv=data['ccv']
            card.expiration_date=data['expiration_date']
            card_serializer = CardSerializer(card)
            return Response(card_serializer.data,status.HTTP_200_OK)
        else:
            return Response({"error_messages":["Pin incorrecto",]},status.HTTP_403_FORBIDDEN)
