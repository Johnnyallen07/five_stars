import base64
import json
import os

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, render, redirect, reverse
from five_stars.models import CustomUser
from teacher.forms import TeacherForm, TeacherScheduleForm
from teacher.models import Teacher, TeacherSchedule, TeacherDisplay
from user.models import UserSchedule

'''
Teacher App Views include all pages excluding dashboard: 
teacher page (displayed in each home box) 
teacher profile, 
teacher schedule
'''
def teacher_page(request, teacher_id):
    user_id = request.session.get('id')
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    subjects_list = teacher.subjects.split(',')
    try:
        teacher_schedule = TeacherSchedule.objects.get(teacher=teacher)
    except TeacherSchedule.DoesNotExist:
        teacher_schedule = TeacherSchedule()
        teacher_schedule.teacher = teacher
    try:
        slots_list = teacher_schedule.available_slots
    except TeacherSchedule.DoesNotExist:
        slots_list = []

    teacher_image_url = get_object_or_404(CustomUser, id=teacher_id).image.url

    if request.method == 'POST':

        # add username to teacher slot, add teacher_name to user slot
        reserved_slot: dict = json.loads(request.POST['slot'])

        user = get_object_or_404(CustomUser, id=user_id)
        try:
            user_schedule = UserSchedule.objects.get(user=user)
        except UserSchedule.DoesNotExist:
            user_schedule = UserSchedule(user=user)
        try:
            user_reserved_slots = user_schedule.reserved_slots
        except TeacherSchedule.DoesNotExist:
            user_reserved_slots = []

        user_reserved_slot = reserved_slot | {'teacher': teacher.teacher_name}
        user_reserved_slots.append(user_reserved_slot)
        user_schedule.reserved_slots = user_reserved_slots
        user_schedule.save()

        # save to teacher schedules
        subject = request.POST['subject']
        teacher_reserved_slot = reserved_slot | {'subject': subject, 'student': user.username}

        # delete the available slot
        slots_list.remove(reserved_slot)
        try:
            teacher_reserved_slots = teacher_schedule.reserved_slots
        except TeacherSchedule.DoesNotExist:
            teacher_reserved_slots = []

        teacher_reserved_slots.append(teacher_reserved_slot)

        teacher_schedule.available_slots = slots_list
        teacher_schedule.reversed_slots = teacher_reserved_slots

        teacher_schedule.save()

    return render(request, 'teacher_page.html', {'teacher': teacher, 'teacher_image_url': teacher_image_url,
                                                 'subjects': subjects_list, 'slots': slots_list})


def teacher_profile(request):
    teacher_id = request.session.get('id')
    user = request.user
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    teacher_display = TeacherDisplay.objects.get(teacher=teacher)
    teacher_image = get_object_or_404(CustomUser, id=teacher_id).image
    teacher_image_url = teacher_image.url
    default_image_url = '/media/user_images/default.png'

    # Check if teacher_image exists and the file exists on the server
    if not (teacher_image and os.path.exists(teacher_image.path)):
        teacher_image_url = default_image_url

    subjects_list = teacher.subjects.split(',')
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the cleaned data
            cleaned_data = form.cleaned_data

            image_data = request.POST.get('image')
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            if user.image and os.path.exists(user.image.path):
                os.remove(user.image.path)

            image = ContentFile(base64.b64decode(imgstr), name=f"""teacher_{user.get_username()}.{ext}""")
            user.image = image
            user.save()

            # Save the rest of the data to Teacher and TeacherDisplay
            teacher_data = cleaned_data.copy()
            teacher_data['teacher_id'] = user.id
            Teacher.objects.update_or_create(
                teacher_id=user.id,
                defaults=teacher_data
            )

            teacher_display.brief_introduction = cleaned_data['brief_introduction']
            teacher_display.brief_subjects = cleaned_data['brief_subjects']
            teacher_display.save()
            return redirect('dashboard')
        else:
            return render(request, 'teacher_profile.html',
                          {'subjects': subjects_list, 'form': form, 'teacher_image_url': teacher_image_url,})
    else:
        form = TeacherForm(instance=teacher, teacher_display_instance=teacher_display, user_instance=user)

    return render(request, 'teacher_profile.html',
                  {'subjects': subjects_list, 'form': form, 'teacher_image_url': teacher_image_url})


def teacher_schedule_view(request):
    teacher_id = request.session.get('id')
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    # Try to get the existing schedule or initialize to None
    try:
        schedule = TeacherSchedule.objects.get(teacher=teacher)
    except TeacherSchedule.DoesNotExist:
        schedule = TeacherSchedule()
        schedule.teacher = teacher

    if request.method == 'POST':
        slots_data = request.POST.get('slots')
        slots = json.loads(slots_data)

        schedule.available_slots = slots

        schedule.save()
        return redirect('dashboard')

    else:
        # Prepare the existing slots for rendering in the template
        slots_json = json.dumps(schedule.available_slots) if schedule else '[]'
        return render(request, 'teacher_schedule.html', {'schedule': schedule, 'slots_json': slots_json})
