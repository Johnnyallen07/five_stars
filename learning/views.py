from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Course, MaterialPost


# Create your views here.
def course_layout_view(request, course):
    topics = course.topics.all()
    return render(request, 'course_layout.html', {'topics': topics, 'course': course})


def course_access(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    # Check if the user is authenticated and has purchased the course
    if request.user.is_authenticated and course in request.user.subscriptions.all():
        # If the user has access, redirect to the topics page
        return course_layout_view(request, course)
    else:
        # If the user hasn't purchased the course, redirect to the purchase page
        return redirect(reverse('purchase'))


def material_page(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    posts = MaterialPost.objects.filter(course_title=course).all()
    context = {'posts': posts, 'postsLen': posts.count(), 'course': course}
    return render(request, 'material_page.html', context)
