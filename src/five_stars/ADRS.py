import os
import django
from django.db import connection

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "five_stars.settings")

# Setup Django
django.setup()


import os
import django
from django.db import connection

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "five_stars.settings")

# Setup Django
django.setup()

# Execute raw SQL query to get all table names
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM teacher_teacher;")
