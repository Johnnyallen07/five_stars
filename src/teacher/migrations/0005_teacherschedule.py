# Generated by Django 5.1.1 on 2024-10-03 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_alter_teacher_teacher_id_alter_teacher_teacher_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slots', models.JSONField(default=list)),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher')),
            ],
        ),
    ]
