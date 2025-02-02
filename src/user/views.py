import json
from datetime import datetime

from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import UserSchedule

"""
User App Views include all pages excluding homepage: 
user profile 
user dashboard (my learning page currently), 
"""


def user_profile(request):
    user_id = request.session.get("id")
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Optionally add a success message or redirect
            return redirect("home")
        else:
            return render(request, "user_profile.html", {"form": form})
    else:
        form = UserForm(instance=user)
        return render(request, "user_profile.html", {"form": form})


def user_dashboard(request):
    # TODO: add default when the user registered
    user_id = request.session.get("id")
    user = get_object_or_404(CustomUser, id=user_id)
    try:
        user_schedule = UserSchedule.objects.get(user=user)
    except UserSchedule.DoesNotExist:
        user_schedule = UserSchedule(user=user)
    try:
        user_missed_slots = user_schedule.missed_slots
    except UserSchedule.DoesNotExist:
        user_missed_slots = []
    try:
        reserved_slots = user_schedule.reserved_slots
    except UserSchedule.DoesNotExist:
        reserved_slots = []

    now = timezone.now()
    upcoming_slots = []
    completed_slots = user_schedule.completed_slots
    total_courses_taken = len(completed_slots)

    if reserved_slots:
        for slot in reserved_slots:
            date_str = slot["end"]
            date_format = "%Y-%m-%dT%H:%M"

            # Convert the string to a datetime object
            date_obj = datetime.strptime(date_str, date_format)

            # Make the datetime object timezone-aware
            date_obj = timezone.make_aware(date_obj)

            print(date_obj)  # Output: 2024-10-07 10:10:00+timezone
            if date_obj > now:
                # Course is upcoming
                upcoming_slots.append(slot)
            else:
                completed_slots.append(slot)

        user_schedule.reserved_slots = upcoming_slots
        user_schedule.completed_slots = completed_slots

    if request.method == "POST":
        data = json.loads(request.body)
        print(data)

        status = data["status"]
        if status == "missed":
            # the user and teacher schedule will be changed
            missed_slot = json.loads(data["slot"].replace("'", '"'))
            completed_slots.remove(missed_slot)
            user_missed_slots.append(missed_slot)
            user_schedule.completed_slots = completed_slots
            user_schedule.missed_slots = user_missed_slots

            # teacher_schedule = TeacherSchedule.objects.get(teacher=Teacher.objects.get(teacher_id=user_id))
            # teacher_completed_slots = teacher_schedule.completed_slots
            # teacher_missed_slots = teacher_schedule.missed_slots
            # del missed_slot['teacher']
            # missed_slot['student'] = user.username
            # teacher_missed_slot = missed_slot
            # teacher_completed_slots.remove(missed_slot)
            # teacher_missed_slots.append(teacher_missed_slot)
            #
            # teacher_schedule.completed_slots = teacher_completed_slots
            # teacher_schedule.missed_slots = teacher_missed_slots
            # teacher_schedule.save()

    user_schedule.save()

    return render(
        request,
        "user_dashboard.html",
        {
            "user": user,
            "course_hour_taken": total_courses_taken,
            "upcoming_slots": upcoming_slots,
            "completed_slots": completed_slots,
            "missed_slots": user_missed_slots,
        },
    )
