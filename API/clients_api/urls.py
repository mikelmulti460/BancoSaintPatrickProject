from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('client',views.UserClientApiView, basename='Clientes')

urlpatterns = [
    path('help/', views.HelpApiView.as_view(),name="help"),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))
]
