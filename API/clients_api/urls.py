from django.urls import path, include
from . import views
from bank_accounts_api.views import OperationsApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('clients',views.UserClientsApiView, basename='Clientes')
urlpatterns = [
    path('help/', views.HelpApiView.as_view(),name="help"),
    path('login/', views.UserLoginApiView.as_view()),
    path('client/', views.UserClientApiView.as_view()),
    path('client/cards/',views.CardAPIView.as_view()),
    path('client/cards/<int:pk>/',views.CardAPIView.as_view()),
    path('client/cards/<int:pk_card>/operations/',OperationsApiView.as_view(),name="Operations"),
    path('client/cards/<int:pk_card>/operations/<int:pk>/',OperationsApiView.as_view(),name="Operation"),
    path('', include(router.urls))
]
