import secrets
import uuid

from PIL import Image
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


def save_pf(instance, filename):
    return f'pfs/{secrets.token_urlsafe(16)}.webp'


class AccountManager(BaseUserManager):
    def create_user(self, email, username, display_name, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, display_name=display_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, display_name, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        return self.create_user(email, username, display_name, password, **other_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    display_name = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True, validators=[RegexValidator(r"^[a-z0-9_]+$")])
    email = models.EmailField(unique=True)
    picture = models.ImageField(upload_to=save_pf, default='pfs/default.webp', )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'display_name']

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)
        image = Image.open(self.picture.path)
        image.thumbnail((512, 512))
        image.save(self.picture.path, format='webp')


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    friends = models.ManyToManyField(Account, related_name='friends', blank=True)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)