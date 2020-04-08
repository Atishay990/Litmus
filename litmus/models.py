from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    email = models.EmailField(max_length=150)

    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s' % (self.email,self.signup_confirmation,self.user.password)

    @receiver(post_save,sender=User)
    def update_profile_signal(sender,instance,created, **kwrags):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.email
