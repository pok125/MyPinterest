from django.db import models
from django.contrib.auth import get_user_model
from pins.models import Pin

User = get_user_model()

class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='comment')
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, null=False, related_name='comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)