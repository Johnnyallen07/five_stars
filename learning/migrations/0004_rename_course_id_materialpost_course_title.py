# Generated by Django 5.1.1 on 2024-09-28 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0003_materialpost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='materialpost',
            old_name='course_id',
            new_name='course_title',
        ),
    ]
