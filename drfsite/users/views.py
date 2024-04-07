from django.shortcuts import render
from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
# Create your views here.
class UserAPILogIn(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            if user.password == password:
                return Response({'message': 'Вход выполнен успешно'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

class UserAPISignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password', '')
        if len(password) < 8:
            return Response({'error': 'Пароль должен содержать не менее 8 символов'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()