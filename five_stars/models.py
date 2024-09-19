from django.contrib.auth.models import AbstractUser
from django.db import models
from learning.models import Course


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    subscriptions = models.ManyToManyField(Course, related_name='subscribed_users', blank=True)
    is_teacher = models.BooleanField(default=False)
    def __str__(self):
        return self.username
