# Generated by Django 5.1.1 on 2024-10-03 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_teacherschedule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacherschedule',
            old_name='teacher_id',
            new_name='teacher',
        ),
    ]
