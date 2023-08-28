import django_filters
from django.db.models import Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from .filters import LikeFilter
from .mixins import LikedMixin
from .models import Post, Like
from .serializers import PostSerializer, LikeByDaySerializer
from accounts.pagination import CustomPageNumberPagination


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikesView(generics.ListAPIView):
    queryset = Like.objects.extra(
        select={'date': "date(blog_like.date_of_like)"}
    ).annotate(likes=Count('pk')).order_by('-date_of_like')
    serializer_class = LikeByDaySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filterset_class = LikeFilter
