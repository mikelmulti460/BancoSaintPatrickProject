from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from . import serializers, models, permissions

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
                            "methods":["get",]
                        },
                    },
                },
                "clients":{
                    "description": "Funciones específicas de clientes",
                }
            }
        }

        return Response(views_defined)

class UserClientApiView(viewsets.ModelViewSet):
    serializer_class = serializers.UserClientSerializer
    queryset = models.UserClient.objects.all()
    authentication_classers = (TokenAuthentication,)
    permission_classes = (permissions.UpdateUserData,)

class UserLoginApiView(ObtainAuthToken):
    """ Crea tokens de autenticación de usuario """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES