from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Used for updating default create user behaviour
    """

    def create_user(self, phone_no, password, **kwargs):
        # implement create user logic
        user = self.model(phone_no=phone_no, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_no, password, **kwargs):
        # create superuser
        self.create_user(phone_no, password)


class CustomUser(AbstractUser):
    username = None
    phone_no = models.CharField(unique=True, max_length=20)
    city = models.CharField(max_length=40)
    USERNAME_FIELD = "phone_no"
    objects = CustomUserManager()


# settings.py の AUTH_USER_MODEL を auth.User にする必要あり
# class UserProfile(models.Model):
#     user = models.OneToOneField(
#         "auth.User", related_name="user_profile", on_delete=models.CASCADE
#     )
#     phone_no = models.CharField(unique=True, max_length=20)
#     city = models.CharField(max_length=40)

#     def __str__(self):
#         return self.user.username
