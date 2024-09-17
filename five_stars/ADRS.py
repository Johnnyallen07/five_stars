import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoDist.settings')

# Setup Django
django.setup()

# Now you can import and use Django models
from videoDist.models import Course

# Fetch all course records
courses = Course.objects.all()
for course in courses:
    print(course.course_id, course.title)

