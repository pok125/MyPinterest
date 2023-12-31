from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Usermodel helper class 커스텀
class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
    
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


# User 커스텀
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=20, 
                                unique=True,
                                help_text=_('Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                error_messages={'unique': _('A user with that nickname already exists.')})
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    # superuser생성 시, 필수 입력 정보 설정
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
    

class FollowRecord(models.Model):
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_user')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('following_user', 'followed_user')