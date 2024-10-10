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
    competitions = models.TextField(help_text="Comma-separated list of competitions", default="")
    introduction = models.TextField()

    def __str__(self):
        return self.first_name


class TeacherSchedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    available_slots = models.JSONField(default=list)
    reserved_slots = models.JSONField(default=list)
    completed_slots = models.JSONField(default=list)
    missed_slots = models.JSONField(default=list)

    def __str__(self):
        return f"{self.teacher_id}_schedule"


class TeacherDisplay(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    brief_subjects = models.CharField(max_length=75)
    brief_introduction = models.CharField(max_length=75)

    def __str__(self):
        return f"{self.teacher_id}_brief_info"
