from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, CreateAPIView
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UsersListSerializer, LoginSerializer
from users.models import User

class UserRegisterView(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserRegisterSerializer
    queryset = get_user_model().objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.perform_create(serializer)

            # add tokens
            refresh = RefreshToken.for_user(user)
            res = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            return Response(res, status=status.HTTP_201_CREATED)


class UsersListView(ListAPIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = UsersListSerializer
    queryset = get_user_model().objects.all()

    def get(self, request):
        users = get_user_model().objects.all()
        serializer = UsersListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


import re

# function that validate whether a value is email or phone
def validate_email_or_phone(value, check_type=None):
    if re.match(r"^\+?1?\d{9,15}$", value):
        check_type = "phone"
        return check_type
    elif re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value):
        check_type = "email"
        return check_type
    else:
        return "Invalid email or phone number."


class LoginView(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = request.POST.get("email")
            data = validate_email_or_phone(email)
            if data == "email":
                user = User.objects.get(email=email)
                print("user", user.email)
                print("type", data)
                user_login = authenticate(
                    email=request.POST.get("email"),
                    password=request.POST.get("password"),
                    backend="users.authenticate.EmailModelBackend",
                )
                refresh = RefreshToken.for_user(user_login)
                auth_login(request, user_login)

                res = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(res, status=status.HTTP_200_OK)
            
            elif data == "phone":
                user = User.objects.get(phone=email)
                print("user", user.phone)

                print("type", data)
                user_login = authenticate(
                    phone=request.POST.get("email"),
                    password=request.POST.get("password"),
                    backend="users.authenticate.PhoneModelBackend",
                )
                refresh = RefreshToken.for_user(user_login)
                auth_login(request, user_login)
                res = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
