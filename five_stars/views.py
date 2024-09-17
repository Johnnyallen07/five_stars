from .models import Topic, Course
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

def course_layout_view(request, course):
    topics = course.topics.all()
    return render(request, 'course_layout.html', {'topics': topics})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('learn')  # Redirect to a page after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def learn_view(request):
    courses = Course.objects.all()
    return render(request, 'learn.html', {'courses': courses})


def course_access(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)

    # Check if the user is authenticated and has purchased the course
    if request.user.is_authenticated and course in request.user.subscriptions.all():
        # If the user has access, redirect to the topics page
        return course_layout_view(request, course)
    else:
        # If the user hasn't purchased the course, redirect to the purchase page
        return redirect(reverse('purchase'))


def purchase(request):
    return render(request, 'purchase.html')


def home_page(request):
    return render(request, 'index.html')