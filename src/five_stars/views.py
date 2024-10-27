import base64
from django.http import HttpRequest, QueryDict
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.core.files.base import ContentFile

from learning.models import Course
from teacher.forms import TeacherForm
from teacher.models import Teacher, TeacherSchedule, TeacherDisplay
from .forms import RegisterForm, TeacherRegisterForm
from django.shortcuts import render, redirect, get_object_or_404, reverse

from .models import CustomUser

"""
Main App Views include: register/teacher-register, login, homepage/dashboard (User/Teacher)
"""


def login_view(request: HttpRequest):
    # simple login view, send id to global session (for necessary url hidden)
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session["id"] = user.id
            if user.is_teacher:
                return redirect("dashboard")
            else:
                return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def to_login_data(data: QueryDict) -> QueryDict:
    result = QueryDict(mutable=True)
    result["csrfmiddlewaretoken"] = data["csrfmiddlewaretoken"]
    result["username"] = data["username"]
    result["password"] = data["password1"]
    return result


def register_view(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # auto login
            auth_form = AuthenticationForm(data=to_login_data(request.POST))
            auth_form.is_valid()
            user = auth_form.get_user()
            login(request, user)
            request.session["id"] = user.id
            if user.is_teacher:
                return redirect("post_register_teacher")
            else:
                return redirect("post_register_student")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def post_register_teacher_view(request: HttpRequest):
    return render(request, "post_register_teacher.html")


def post_register_student_view(request: HttpRequest):
    return render(request, "post_register_teacher.html")


def teacher_register_view(request: HttpRequest):
    # First teacher register form
    if request.method == "POST":
        form = TeacherRegisterForm(request.POST)

        if form.is_valid():
            teacher_form_data = form.cleaned_data
            request.session["teacher_form_data"] = teacher_form_data
            return redirect("teacher-register-profile")
    else:
        form = TeacherRegisterForm()

    return render(request, "teacher_register.html", {"form": form})


def teacher_register_profile(request: HttpRequest):
    # TODO: add default init like TeacherSchedule...
    teacher_form_data = request.session.get("teacher_form_data")
    teacher_image_url = "/media/user_images/default.png"
    if request.method == "POST":
        data = request.POST.copy()
        data["username"] = teacher_form_data["username"]
        profile_form = TeacherForm(data)

        if profile_form.is_valid():
            # TODO: wrap image data to utils
            image_data = request.POST.get("image")
            format, imgstr = image_data.split(";base64,")
            ext = format.split("/")[-1]

            # teacher form depends on the customUser for login
            teacher_user = CustomUser(
                username=teacher_form_data["username"],
                email=teacher_form_data["email"],
                is_teacher=True,
            )

            image = ContentFile(
                base64.b64decode(imgstr), name=f"""teacher_{teacher_user.id}.{ext}"""
            )
            teacher_user.image = image
            teacher_user.set_password(teacher_form_data["password2"])
            teacher_user.save()

            # profile form depends on the Teacher Model
            teacher = profile_form.save(commit=False)
            teacher.teacher_id = teacher_user.id
            teacher.teacher_name = teacher_form_data.get("username")
            teacher.email = teacher_form_data.get("email")

            # add default competition field
            teacher.competitions = ""

            teacher.save()

            # save to teacher_display model
            teacher_display = TeacherDisplay(
                teacher=teacher,
                brief_subjects=profile_form.cleaned_data["brief_subjects"],
                brief_introduction=profile_form.cleaned_data["brief_introduction"],
            )
            teacher_display.save()

            del request.session["teacher_form_data"]
            return redirect("login")
        else:
            return render(
                request,
                "teacher_register_profile.html",
                {"form": profile_form, "teacher_image_url": teacher_image_url},
            )

    else:
        profile_form = TeacherForm()

    return render(
        request,
        "teacher_register_profile.html",
        {"form": profile_form, "teacher_image_url": teacher_image_url},
    )


def purchase_view(request: HttpRequest):
    return render(request, "purchase.html")


def index_page_view(request: HttpRequest):
    return render(request, "index.html")


def home_view(request: HttpRequest):
    user = CustomUser.objects.get(id=request.session.get("id"))
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    teacher_display_list = []

    for teacher in teachers:
        teacher_id = teacher.teacher_id
        teacher_display = TeacherDisplay.objects.get(teacher=teacher)
        print(CustomUser.objects.get(id=teacher_id).image.url)
        teacher_display_list.append(
            {
                "teacher_id": teacher_id,
                "teacher_image": CustomUser.objects.get(id=teacher_id).image.url,
                "teacher_name": teacher.teacher_name,
                "school": teacher.school,
                "brief_subjects": teacher_display.brief_subjects
                if teacher_display
                else "",
                "brief_introduction": teacher_display.brief_introduction
                if teacher_display
                else "",
            }
        )

    return render(
        request,
        "home.html",
        {
            "courses": courses,
            "user": user,
            "teacher_display_list": teacher_display_list,
        },
    )


def teacher_dashboard_view(request: HttpRequest):
    # TODO: add default when the teacher registered, wrap the method below
    teacher_id = request.session.get("id")
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    try:
        teacher_schedule = TeacherSchedule.objects.get(teacher=teacher)
    except TeacherSchedule.DoesNotExist:
        teacher_schedule = TeacherSchedule(teacher=teacher)

    try:
        reserved_slots = teacher_schedule.reserved_slots
    except TeacherSchedule.DoesNotExist:
        reserved_slots = []

    missed_slots = teacher_schedule.missed_slots

    now = timezone.now()
    upcoming_slots = []
    completed_slots = teacher_schedule.completed_slots
    total_courses_taken = len(completed_slots)

    if reserved_slots:
        for slot in reserved_slots:
            date_str = slot["end"]
            date_format = "%Y-%m-%dT%H:%M"
            date_obj = datetime.strptime(date_str, date_format)
            date_obj = timezone.make_aware(date_obj)
            if date_obj > now:
                upcoming_slots.append(slot)
            else:
                completed_slots.append(slot)

        teacher_schedule.reserved_slots = upcoming_slots
        teacher_schedule.completed_slots = completed_slots

    teacher_schedule.save()

    return render(
        request,
        "dashboard.html",
        {
            "teacher": teacher,
            "course_hour_taken": total_courses_taken,
            "reserved_slots": upcoming_slots,
            "completed_slots": completed_slots,
            "missed_slots": missed_slots,
        },
    )
