from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, generics, permissions, status, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

# from masters.models import MasterModel
# from products.models import HouseModel
# from store.models import StoreModel
from .models import User, Map

# from products.serializers import HomeSerializer
# from masters.serializers import MasterSerializer
# from store.serializers import StoreModelSerializer

from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer, UserALLSerializer, \
    UpdateUserSerializer, MapSerializer


class UserViewSet(GenericViewSet):
    ''' Регистрация юзера '''
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    # @action(['POST'], detail=False, permission_classes=[permissions.AllowAny])
    def create(self, request: Request):
        self.serializer_class = RegistrationSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        password = serializer.validated_data['password']
        token, created = User.objects.get_or_create(phone_number=phone_number, first_name=first_name,
                                                    last_name=last_name, password=password)
        return Response({'token': token.tokens()})

    #
    # @action(['DELETE'], detail=False, permission_classes=[IsAuthenticated])
    # def logout(self, request: Request):
    #     Token.objects.get(user=request.user).delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# class LoginView(TokenObtainPairView):
# permission_classes = (AllowAny,)
# serializer_class = MyTokenObtainPairSerializer
# from django.contrib.auth import login, authenticate
#
#
# class LoginView(APIView):
#     def post(self, request):
#         phone_number = request.data['phone_number']
#         password = request.data['password']
#         user = authenticate(phone=phone_number, password=password)
#         if not user:
#             login(request, user)

# class LoginView(viewsets.ViewSet):
#     """ Elektron pochta va parolni tekshiradi va autentifikatsiya belgisini qaytaradi."""
#
#     serializer_class = AuthTokenSerializer
#
#     def create(self, request):
#         """Tokenni tasdiqlash va yaratish uchun ObtainAuthToken APIView-dan foydalaning."""
#
#         return ObtainAuthToken().as_view()(request=request._request)
class LoginView(GenericViewSet):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    @action(['POST'], detail=False, permission_classes=[permissions.AllowAny])
    def login(self, request: Request):
        self.serializer_class = LoginSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': 'User with this phone number does not exist'})
        if int(code) == int(User.objects.get(phone_number=phone_number).mycode):

            token, created = User.objects.get_or_create(phone_number=phone_number)
            return Response({'token': token.tokens()})
        else:
            return Response(
                {'error': f"Code is not valid! {code}=!{User.objects.get(phone_number=phone_number).mycode}"})

    @action(['POST'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        if not token.blacklist():
            return Response("Ошибка")
        else:
            return Response({"status": "Успешно"})


class UserProfile(APIView):
    get_serializer_class = None

    def get_object(self, user, pk=None):
        pass

    def get(self, request, **kwargs):
        pass
        # return Response(data, status=200)


class UserList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        users = User.objects.get(id=pk)
        serializer = UserSerializer(users, context={'request': request})
        return Response(serializer.data)


# class UserProductsList(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request, pk):
#         users = CustomUser.objects.get(id=pk)
#         serializer = UserProductsSerializer(users, context={'request': request})
#         return Response(serializer.data)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UpdateProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UpdateUserSerializer


class UserProfileList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        users = User.objects.filter(id=pk)
        serializer = UserSerializer(users, context={'request': request}, many=True)
        return Response(serializer.data)


class MapView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
              mixins.DestroyModelMixin, GenericViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = (IsAuthenticated, )
