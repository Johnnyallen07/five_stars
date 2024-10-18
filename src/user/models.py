from django.db import models

from five_stars.models import CustomUser


# Create your models here.
class UserSchedule(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reserved_slots = models.JSONField(default=list)
    completed_slots = models.JSONField(default=list)
    missed_slots = models.JSONField(default=list)

    def __str__(self):
        return f"{self.user_id}_schedule"
