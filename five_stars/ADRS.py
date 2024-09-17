import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'five_stars.settings')

# Setup Django
django.setup()

from django.db import connection

# Execute raw SQL query
with connection.cursor() as cursor:
    pass
    rows = cursor.fetchall()

# Output the result
for row in rows:
    print(row)


