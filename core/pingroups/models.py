from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PinGroup(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name="pingroup"
    )
    title = models.CharField(
        max_length=50, null=False, help_text="50자 이내로 작성해주세요.(필수)"
    )
    image = models.ImageField(upload_to="pingroups/", null=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
