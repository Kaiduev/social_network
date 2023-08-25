from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from .views import (
    UserViewSet
)


urlpatterns = [
    path('sign-up/', UserViewSet.as_view({"post": "create"}), name="sign_up"),
    path('users/', UserViewSet.as_view({'get': 'list'}), name='users'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
