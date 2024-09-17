from django.db import models


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image_url = models.URLField(max_length=200,
                                default='https://cdn.pixabay.com/photo/2015/11/15/07/47/geometry-1044090_1280.jpg')

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, related_name="topics", on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.title


class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, related_name="subtopics", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True)  # Assuming videos are external, like YouTube

    def __str__(self):
        return self.title
