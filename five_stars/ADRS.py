import os
import django
from django.db import connection

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'five_stars.settings')

# Setup Django
django.setup()


import os
import django
from django.db import connection

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'five_stars.settings')

# Setup Django
django.setup()

# Execute raw SQL query to get all table names
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = cursor.fetchall()

# Output the table names
for table in tables:
    print(table[0])

# Execute raw SQL query
with connection.cursor() as cursor:
    # Rename the column
    cursor.execute('SELECT * FROM teacher_teacher')
    rows = cursor.fetchall()

# Output the table names
for row in rows:
    print(row[0])

