from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


### Usermodel helper class 커스텀
class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True

        return self._create_user(email, password, **extra_fields)


### User 커스텀
class User(AbstractBaseUser):
    email = models.EmailField(
        _("email address"), unique=True, max_length=100, null=False, blank=False
    )
    password = models.CharField(max_length=20, null=False, blank=False)
    nickname = models.CharField(
        max_length=10,
        unique=True,
        null=False,
        blank=False,
        help_text=_("Required. 10 characters or fewer. Letters, digits only."),
        error_messages={"unique": _("A user with that nickname already exists.")},
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    following = models.ManyToManyField(
        "self",
        through="Follow",
        related_name="followers",
        symmetrical=False,
        verbose_name=_("following users"),
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # superuser생성 시, 필수 입력 정보 설정
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return self.followers.count()

    def __str__(self):
        return self.nickname


### Follow 모델
class Follow(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name="following_relations",
        on_delete=models.CASCADE,
        verbose_name=_("from user"),
    )
    to_user = models.ForeignKey(
        User,
        related_name="follower_relations",
        on_delete=models.CASCADE,
        verbose_name=_("to user"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")
        constraints = [
            models.CheckConstraint(
                check=~models.Q(from_user=models.F("to_user")),
                name="prevent_self_follow",
            )
        ]
        verbose_name = _("Follow")
        verbose_name_plural = _("Follows")

    def __str__(self):
        return f"{self.from_user.nickname} follows {self.to_user.nickname}"
