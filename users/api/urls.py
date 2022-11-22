from django.urls import path
from .views import *

app_name = "api"


urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("users/", UsersListView.as_view(), name="users"),
    path("login/", LoginView.as_view(), name="login")
]