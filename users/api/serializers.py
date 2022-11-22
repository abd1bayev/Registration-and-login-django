from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions, status
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate



UserModel = get_user_model()

phone_regex = RegexValidator(
    regex=r"^233\d{2}\s*?\d{3}\s*?\d{4}$",
    message=_("Invalid phone number."),
)

class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "phone",
            "first_name",
            "last_name",
            "date_joined",
        ]


# Register user with either email or phone
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    phone = serializers.CharField(validators=[phone_regex])

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
        ]

    def __init__(self, *args, **kwargs):
        super(UserRegisterSerializer, self).__init__(*args, **kwargs)
        self.fields["phone"] = serializers.HiddenField(default="", validators=[phone_regex])

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        check_value_type = validate_email_or_phone(email)
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)

        print("username_field1", self.username_field)

        if check_value_type == "phone":
            if self.username_field == (UserModel._meta.get_field("email")):
                self.username_field = UserModel._meta.get_field("phone")
                validated_data["phone"] = email

            user = get_user_model().objects.create_user(**validated_data)
            user.set_password(password)
            user.email = None
            user.save()
            return user
        elif check_value_type == "email":
            if self.username_field == (UserModel._meta.get_field("phone")):
                self.username_field = UserModel._meta.get_field("email")
                validated_data["email"] = email

            user = get_user_model().objects.create_user(**validated_data)
            user.set_password(password)
            user.phone = None
            user.save()
            return user

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value

    def validate_email(self, value):
        test = validate_email_or_phone(value)
        if test == "phone":
            print("phone")
            if get_user_model().objects.filter(phone=value).exists():
                raise serializers.ValidationError("Phone number already exists.")
        if test == "email":
            print("email")
            if get_user_model().objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists.")

        return value


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
        raise serializers.ValidationError("Invalid email or phone number.")




# Login Serializer
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = authenticate(email=email, password=password)

        if not user:
            raise exceptions.AuthenticationFailed(
                f"We didn't find a Notion account for this {email} address or phone number.",
                status.HTTP_401_UNAUTHORIZED,
            )
        if not user.is_active:
            raise exceptions.AuthenticationFailed("Account disabled, contact admin.")
        return {
            "email": user.email,
            "phone_number": user.phone,
        }