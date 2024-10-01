from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from learning.models import Course
from teacher.forms import TeacherForm
from teacher.models import Teacher
from .forms import RegisterForm, TeacherRegisterForm
from django.shortcuts import render, redirect, get_object_or_404


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
            # retrieve data from the teacher form

            teacher_form = TeacherRegisterForm(teacher_form_data)

            # teacher form depends on the customUser for login
            teacher_user = teacher_form.save()
            # profile form depends on the Teacher Model
            teacher_model = profile_form.save(commit=False)
            teacher_model.teacher_id = teacher_user.id
            teacher_model.teacher_name = teacher_form_data.get('username')
            teacher_model.email = teacher_form_data.get('email')
            teacher_model.save()

            del request.session['teacher_form_data']
            return redirect('login')
        else:
            subjects_string = request.POST.get('subjects', '')
            subjects_list = subjects_string.split(',') if subjects_string else []
            return render(request, 'teacher_register_profile.html', {'form': profile_form, 'subjects': subjects_list})

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
    return render(request, 'dashboard.html', {'teacher': teacher})
