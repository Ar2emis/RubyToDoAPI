from rest_framework import routers
from .views import UserViewSet
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include


user_router = routers.DefaultRouter()

user_router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('token', obtain_auth_token, name='api_token')
] + user_router.urls