from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, permissions
from .models import User
from .models import UserProfile, Role
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from .serializers import TokenSerializer, UserSerializer, ProfileSerializer, RoleSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        # role = request.data.get("role", 1)
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username,password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email,
        )
        querys = User.objects.filter(email=email).values()
        print(querys)
        return Response(data={
            "message": "Account created successfully",
            "user_details": querys[0]
        },
            status=status.HTTP_201_CREATED)
