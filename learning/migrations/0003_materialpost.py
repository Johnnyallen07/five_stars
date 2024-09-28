# Generated by Django 5.1.1 on 2024-09-28 10:33

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0002_alter_course_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('file_path', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='learning.course')),
            ],
        ),
    ]
