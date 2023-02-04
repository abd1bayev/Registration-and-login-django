from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import UserProfile, UserList, UpdateProfileView, UserViewSet, LoginView, UserProfileList, \
        MapView

router = DefaultRouter()
router.register('', LoginView, 'auth')
router.register('signup', UserViewSet, 'register')
router.register('map', MapView, 'map')

urlpatterns = [
        # path('api/v1/users/', include('user.urls')),
        path('api/v1/profile/<int:pk>/', UserProfileList.as_view()),
        # path('api/v1/user-products/<int:pk>/', UserProductsList.as_view()),
        path('api-auth/', include('rest_framework.urls')),
        path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('api/v1/update-user/<int:pk>/', UpdateProfileView.as_view()),
        path('profile/', UserProfile.as_view(), name='user-profile'),
]

urlpatterns += router.urls
