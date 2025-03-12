from django.urls import path
from .views import AuthAPIView, SignupAPIView, ListUserAPIView, JWKSView


urlpatterns = [
    path('', ListUserAPIView.as_view(), name='users'),
    path('jwks', JWKSView.as_view(), name='jwks'),
    path('auth', AuthAPIView.as_view(), name='auth'),
    path('signup', SignupAPIView.as_view(), name='signup'),
]
