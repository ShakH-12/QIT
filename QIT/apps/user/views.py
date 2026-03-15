from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, ResponseSerializer


def custom_404(request, exception):
    return render(request, '404.html')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(ResponseSerializer(user).data)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(ResponseSerializer(request.user).data)