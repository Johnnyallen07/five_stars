# Generated by Django 5.1.1 on 2024-09-30 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_remove_teacher_id_teacher_teacher_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='teacher_name',
            field=models.CharField(default='johnny', max_length=100),
        ),
    ]
