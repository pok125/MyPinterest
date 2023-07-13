from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        
        # 내 현재 국가 시간
        now = timezone.localtime()
        email = self.normalize_email(email)
        date_joined = now
        user = self.model(email=email, date_joined=date_joined, **extra_fields)
        user.set_passwrod(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(
        max_length=20,
        unique=True,
        help_text=_(
            'Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    following_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email