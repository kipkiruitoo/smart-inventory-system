from rest_framework import serializers
from .models import User, UserProfile, Role

from django.contrib.auth.models import Group


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", 'groups')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('user', 'telephone',  'postaladdress', 'name', 'role',
                  'county', 'subcounty', 'constituency', 'ward', 'employee_gender', 'employee_id_number', 'photo')


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'description')
