from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q



UserModel = get_user_model()

#Login user with either email or phone_number
class EmailModelBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            if email is None:
                email = kwargs.get(UserModel.USERNAME_FIELD)
            if email is None and password is None:
                return
            user = UserModel._default_manager.get(email=email)
            print("backend", user.email)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            





class PhoneModelBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            if phone is None:
                phone = kwargs.get(UserModel.USERNAME_FIELD)
            if phone is None and password is None:
                return
            user = UserModel._default_manager.filter(phone=phone).first()
            # print("backend", user.phone)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            

# class EmailOrPhoneModelBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             user = UserModel._default_manager.get(
#                 Q(email=email) | Q(phone=email)
#             )
#         except UserModel.DoesNotExist:
#             UserModel().set_password(password)

#         else:
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user
 