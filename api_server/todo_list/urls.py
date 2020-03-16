from rest_framework import routers
from .views import ProjectViewSet, TaskViewSet
from django.urls import path, include


project_router = routers.DefaultRouter()

project_router.register(r'projects', ProjectViewSet, basename='project')
project_router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = project_router.urls