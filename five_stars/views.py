from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

from learning.models import Course
from learning.views import course_layout_view
from teacher.models import Teacher
from .forms import RegisterForm, TeacherRegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import CustomUser


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_teacher:
                request.session['teacher_id'] = user.id
                return redirect('dashboard')
            else:
                return redirect('home')
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


def teacher_register_view(request):
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect after successful registration
    else:
        form = TeacherRegisterForm()

    return render(request, 'teacher_register.html', {'form': form})


def purchase(request):
    return render(request, 'purchase.html')


def home_page(request):
    return render(request, 'index.html')


def home_view(request):
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'home.html', {'courses': courses, 'teachers': teachers})


def dashboard_view(request):
    teacher_id = request.session.get('teacher_id')
    teacher = get_object_or_404(CustomUser, id=teacher_id)
    return render(request, 'dashboard.html', {'teacher': teacher})