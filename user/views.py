import json
from rest_framework import generics
from .serializers import AuthSerializer, SignupSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
from jwcrypto import jwk
from rest_framework.views import APIView
from django.conf import settings



class JWKSView(APIView):

    permission_classes = []
    def get(self, request):
        public_key = jwk.JWK.from_pem(settings.SIMPLE_JWT["VERIFYING_KEY"].encode('utf8'))
        jwk_set = {
            "keys": [json.loads(public_key.export())]
        }
        return Response(jwk_set)


class AuthAPIView(generics.CreateAPIView):
    serializer_class = AuthSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "User created successfully"})
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

class ListUserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
