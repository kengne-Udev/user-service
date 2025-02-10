from django.urls import path
from .views import AuthAPIView, SignupAPIView, ListUserAPIView


urlpatterns = [
    path('', ListUserAPIView.as_view(), name='users'),
    path('auth', AuthAPIView.as_view(), name='auth'),
    path('signup', SignupAPIView.as_view(), name='signup'),
]
