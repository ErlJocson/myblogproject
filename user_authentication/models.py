from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ngettext_lazy as _
from django.contrib.auth.models import AbstractUser


# managers
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


# the user class already has first_name, last_name, and password
class User(AbstractUser):
    username = models.CharField(max_length=24, unique=True)
    email = models.CharField(max_length=80, unique=True)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="media/profile_pictures", blank=True, null=True)

    def __str__(self):
        return self.username
