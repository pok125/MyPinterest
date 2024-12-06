from django.contrib.auth import get_user_model
from django.db import models
from pingroups.models import PinGroup

User = get_user_model()


class Pin(models.Model):
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name="pin"
    )
    group = models.ForeignKey(
        PinGroup, on_delete=models.CASCADE, null=False, related_name="pin"
    )
    image = models.ImageField(upload_to="pins/", null=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField()
    likers = models.ManyToManyField(
        User,
        related_name="liked_pins",
        through="LikeRecord",
        verbose_name="좋아요한 사용자",
    )
    book_markers = models.ManyToManyField(
        User,
        related_name="bookmarked_pins",
        through="BookMark",
        verbose_name="북마크한 사용자",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return self.likers.count()

    @property
    def book_mark_count(self):
        return self.book_markers.count()


class LikeRecord(models.Model):
    pin = models.ForeignKey(
        Pin, on_delete=models.CASCADE, related_name="pin_likes_record"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_likes_record"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("pin", "user")
        verbose_name = "좋아요 기록"
        verbose_name_plural = "좋아요 기록들"

    def __str__(self):
        return f"{self.user.nickname}이(가) {self.pin.title}을(를) 좋아합니다"


class BookMark(models.Model):
    pin = models.ForeignKey(
        Pin, on_delete=models.CASCADE, related_name="pin_bookmarks_record"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bookmarks_record"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("pin", "user")
        verbose_name = "북마크 기록"
        verbose_name_plural = "북마크 기록들"

    def __str__(self):
        return f"{self.user.nickname}이(가) {self.pin.title}을(를) 북마크했습니다"
