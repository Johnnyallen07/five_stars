from django.contrib.auth.models import AbstractUser
from django.db import models
from learning.models import Course

"""
User Model: CustomUser overrides Authorized User
"""


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    subscriptions = models.ManyToManyField(
        Course, related_name="subscribed_users", blank=True
    )
    is_teacher = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to="user_images/", default="default_avatar.png", blank=True, null=True
    )

    def __str__(self):
        return self.username
