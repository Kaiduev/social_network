from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import FanSerializer
from .services import (
    add_like, remove_like, get_fans,
)


class LikedMixin:
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        obj = self.get_object()
        add_like(obj, request.user)
        return Response({'message': 'post liked', 'code': 200}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        obj = self.get_object()
        remove_like(obj, request.user)
        return Response({'message': 'post unliked', 'code': 200}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def get_fans(self, request, pk=None):
        obj = self.get_object()
        fans = get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
