from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import (
    UserSignUpSerializer, UserSerializer
)
from .pagination import CustomPageNumberPagination


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPageNumberPagination
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSignUpSerializer
        return UserSerializer
