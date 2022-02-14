from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('clients',views.UserClientsApiView, basename='Clientes')
urlpatterns = [
    path('help/', views.HelpApiView.as_view(),name="help"),
    path('login/', views.UserLoginApiView.as_view()),
    path('client/', views.UserClientApiView.as_view()),
    path('client/cards/',views.CardAPIView.as_view()),
    path('client/cards/<int:pk>/',views.CardAPIView.as_view()),
    #path('client/operations/'),
    path('', include(router.urls))
]
