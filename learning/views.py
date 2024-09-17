from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Course


# Create your views here.
def course_layout_view(request, course):
    topics = course.topics.all()
    return render(request, 'course_layout.html', {'topics': topics})


def course_access(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)

    # Check if the user is authenticated and has purchased the course
    if request.user.is_authenticated and course in request.user.subscriptions.all():
        # If the user has access, redirect to the topics page
        return course_layout_view(request, course)
    else:
        # If the user hasn't purchased the course, redirect to the purchase page
        return redirect(reverse('purchase'))


def home_view(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})