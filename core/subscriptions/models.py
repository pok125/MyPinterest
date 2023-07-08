from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='subscription', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='subscription', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project')

