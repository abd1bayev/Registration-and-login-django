from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager

# Create your models here.


class User(AbstractUser, PermissionsMixin):
    username = None
    phone_regex = RegexValidator(
        regex=r"^233\d{2}\s*?\d{3}\s*?\d{4}$",
        message=_("Invalid phone number."),
    )
    # phone = models.CharField(
    #     max_length=15,
    #     validators=[phone_regex],
    #     unique=True,
    #     blank=True,
    #     null=True,
    #     verbose_name=_("phone"),
    # )

    phone = PhoneNumberField(blank=True, null=True)


    # NB: email validation will be done in the serializer
    email = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("email"),
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("first name"),
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("last name"),
    )

    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True
    )  # this is the default field for the user model

    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("date joined"),
    )
    two_step_password = models.BooleanField(
        default=False,
        help_text=_("is active two step password?"),
        verbose_name=_("two step password"),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "phone"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name"]

    def __str__(self):
        return f"{self.phone}"

    # @property
    # def get_full_name(self):
    #     full_name = f"{self.first_name} {self.last_name}"
    #     return full_name.strip()
