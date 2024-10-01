from django.db import models


# Create your models here.
class Teacher(models.Model):
    teacher_id = models.IntegerField(primary_key=True)
    teacher_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    school = models.CharField(max_length=255)
    subjects = models.TextField(help_text="Comma-separated list of subjects")
    introduction = models.TextField()

    def __str__(self):
        return self.first_name
