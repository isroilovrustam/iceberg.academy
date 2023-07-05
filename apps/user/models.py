from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from config import settings
from .permissions import CustomPermissionsMixin

phone_regex = RegexValidator(
    regex=r"^998[378]{2}|9[01345789]\d{7}$",
    message="Phone number must be entered in the format: '998 [XX] [XXX XX XX]'. Up to 12 digits allowed."
)


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **kwargs):
        if not phone:
            raise TypeError('Username did not come')
        if password is None:
            password = '1'
        user = self.model(phone=phone, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **kwargs):
        if not password:
            raise TypeError('Password did not come')
        user = self.create_user(phone, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, CustomPermissionsMixin):
    name = models.CharField(max_length=255)
    phone = models.CharField(validators=[phone_regex], unique=True, max_length=12)
    image = models.FileField(upload_to='users/', null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.name

    @property
    def image_path(self):
        if self.image:
            return f"{settings.SITE_URL}{self.image.url}"
        return None


class VerifyPhone(models.Model):
    phone = models.CharField(max_length=12)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.phone


class Team(models.Model):
    name = models.CharField(max_length=202)
    image = models.FileField(upload_to='team/')
    profession = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.profession}"

    @property
    def image_path(self):
        if self.image:
            return f"{settings.SITE_URL}{self.image.url}"
        return None
