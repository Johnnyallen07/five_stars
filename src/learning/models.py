from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
from django.dispatch import receiver


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image_url = models.URLField(
        max_length=200,
        default="https://cdn.pixabay.com/photo/2015/11/15/07/47/geometry-1044090_1280.jpg",
    )

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(
        Course, related_name="topics", on_delete=models.CASCADE, default=0
    )

    def __str__(self):
        return self.title


class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, related_name="subtopics", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class MaterialPost(models.Model):
    course_title = models.ForeignKey(
        Course, related_name="materials", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    file_path = models.FileField(upload_to="uploads/", blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


@receiver(models.signals.post_delete, sender=MaterialPost)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file_path:
        if os.path.isfile(instance.file_path.path):
            os.remove(instance.file_path.path)


@receiver(models.signals.pre_save, sender=MaterialPost)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).file_path
    except sender.DoesNotExist:
        return False

    new_file = instance.file_path
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
