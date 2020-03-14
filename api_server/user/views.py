from .serializers import UserSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']
    filter_backends = [DjangoFilterBackend]

    def filter_queryset(self, queryset):

        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)