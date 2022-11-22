from django.contrib.auth.models import BaseUserManager


# Create user with either email or phone number
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email and not phone:
            raise ValueError("Users must have an email or phone number")
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            last_name=last_name,
            first_name=first_name,
        )
        user.set_password(password)
        user.save(using=self._db,)
        return user

    def create_superuser(self, email, phone, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email) 