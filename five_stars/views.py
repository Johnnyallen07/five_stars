import base64
import json

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.http import JsonResponse

from learning.models import Course
from teacher.forms import TeacherForm
from teacher.models import Teacher, TeacherSchedule
from . import settings
from .forms import RegisterForm, TeacherRegisterForm
from django.shortcuts import render, redirect, get_object_or_404, reverse

from .models import CustomUser


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['id'] = user.id
            if user.is_teacher:
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
            teacher_form_data = form.cleaned_data
            request.session['teacher_form_data'] = teacher_form_data
            return redirect('teacher-register-profile')
    else:
        form = TeacherRegisterForm()

    return render(request, 'teacher_register.html', {'form': form})


def teacher_register_profile(request):
    teacher_form_data = request.session.get('teacher_form_data')
    if request.method == 'POST':
        profile_form = TeacherForm(request.POST)

        if profile_form.is_valid():

            image_data = request.POST.get('image')
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(imgstr), name=f"""teacher_{teacher_form_data['username']}.{ext}""")

            # teacher form depends on the customUser for login
            teacher_user = CustomUser(
                username=teacher_form_data['username'],
                email=teacher_form_data['email'],
                image=image,
                is_teacher=True
            )
            teacher_user.set_password(teacher_form_data['password2'])
            teacher_user.save()

            # profile form depends on the Teacher Model
            teacher = profile_form.save(commit=False)
            teacher.teacher_id = teacher_user.id
            teacher.teacher_name = teacher_form_data.get('username')
            teacher.email = teacher_form_data.get('email')
            teacher.save()

            del request.session['teacher_form_data']
            return redirect('login')
        else:
            return render(request, 'teacher_register_profile.html', {'form': profile_form})

    else:
        profile_form = TeacherForm()

    return render(request, 'teacher_register_profile.html', {'form': profile_form})


def purchase(request):
    return render(request, 'purchase.html')


def home_page(request):
    return render(request, 'index.html')


def home_view(request):
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'home.html', {'courses': courses, 'teachers': teachers})


def dashboard_view(request):
    teacher_id = request.session.get('id')
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    teacher_schedule = get_object_or_404(TeacherSchedule, teacher=teacher)
    # teacher_schedule_json = json.dumps(teacher_schedule.available_slots) if teacher_schedule else '[]'
    return render(request, 'dashboard.html',
                  {'teacher': teacher,
                   'teacher_schedule': teacher_schedule,
                   'reserved_slots': teacher_schedule.reserved_slots})
