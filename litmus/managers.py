from django.contrib.auth.models import BaseUserManager
from django.conf import settings
User = settings.AUTH_USER_MODEL



class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
          if not email:
            raise ValueError('Email field is required')

          email = self.normalize_email(email)
          user = self.model(email=email, **kwargs)
          user.set_password(password)
          user.save()
          return user

    def create_superuser(self, email, password, **extra_fields):

          extra_fields.setdefault('is_staff', True)
          extra_fields.setdefault('is_superuser', True)
          extra_fields.setdefault('is_active', True)
          return self.create_user(email, password, **extra_fields)
