from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, LikesView

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('analytics/', LikesView.as_view(), name='analytics')
]
urlpatterns += router.urls
