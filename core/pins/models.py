from django.db import models
from django.contrib.auth import get_user_model
from pingroups.models import PinGroup

User = get_user_model()

class Pin(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='pin')
    group = models.ForeignKey(PinGroup, on_delete=models.CASCADE, null=False, related_name='pin')
    image = models.ImageField(upload_to='pins/', null=False)
    title = models.CharField(max_length=50)
    content = models.TextField()
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LikeRecord(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='like_record')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_record')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pin', 'user')


class BookMark(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='book_mark')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_mark')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pin', 'user')