from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MyAccountManager(BaseUserManager):

    def created_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address.")
        if not username:
            raise ValueError("User must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.created_user(
            email=self.normalize_email(email),
            username=username,
            password=password,

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return f'profiles_images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return "projectimages/010.jpg"


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    data_Joined = models.DateTimeField(verbose_name="data Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profiles_images/{self.pk}/'):]

    def has_perm(self, perm, object=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **Kwargs):
    if created:
        Token.objects.create(user=instance)
