from collections import defaultdict

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from masters.serializers import MasterSerializer
# from mebel.serializers import AllMebelSerializer
# from products.serializers import HomeSerializer, NewAllWebHomeCreateSerializer
# from store.serializers import StoreModelSerializer, ProfileStoreModelSerializer
from .models import User, Map
from ..products.serializers import ProductSerializer


class CheckTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=130, required=False)
    last_name = serializers.CharField(max_length=130, required=False)
    password = serializers.CharField(max_length=130, required=False)
    confirm_password = serializers.CharField(max_length=130, required=False)

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name', 'password', 'confirm_password']
        # extra_kwargs = dict(
        #     password=dict(required=True)
        # )

    def validate(self, attrs):
        errors = defaultdict(list)
        # emails = CustomUser.objects.filter(email=attrs['email'])
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        # password2 = attrs.get('password2')
        # if emails.exists():
        #     errors['email'].append('Email has already')
        if errors:
            raise serializers.ValidationError(errors)
        if password != confirm_password:
            raise serializers.ValidationError(
                {'status': "Password do not match"}
            )
        return attrs

    def create(self, validated_data):
        # password1 = validated_data.pop('password1', None)
        # password2 = validated_data.pop('password2', None)
        # if password1:
        #     user.set_password(password1)
        #     user.set_password(password2)
        user = super().create(validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        # password1 = validated_data.pop('password1', None)
        # password2 = validated_data.pop('password2', None)
        # if password1:
        #     user.set_password(password1)
        #     user.set_password(password2)
        user = super().update(instance, validated_data)
        user.save()
        return user


class UserDataSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False,
                                     validators=[validate_password])

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        if password := attrs.get('password'):
            attrs['password'] = make_password(password)
        return attrs


class UserALLSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['user_permissions', 'groups', 'password']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user_data'] = UserDataSerializer(self.user).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'
        extra_kwargs = {"user": {"read_only": True}}

# class UserProductsSerializer(serializers.ModelSerializer):
#     maklers = MasterSerializer(many=True)
#     stores = ProfileStoreModelSerializer(many=True)
#     houses = NewAllWebHomeCreateSerializer(many=True)
#     mebels = AllMebelSerializer(many=True)
#
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'maklers', 'stores', 'houses', 'mebels']


class UpdateUserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'email', 'phone_number', 'password')
        extra_kwargs = {
            'first_name': {'required': False},
            'email': {'required': False},
            'phone_number': {'required': False},
            'password': {'required': False},
        }