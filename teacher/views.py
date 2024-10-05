import base64
import json
import os

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, render, redirect, reverse
from five_stars.models import CustomUser
from teacher.forms import TeacherForm, TeacherScheduleForm
from teacher.models import Teacher, TeacherSchedule


def teacher_page(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    subjects_list = teacher.subjects.split(',')
    schedule = TeacherSchedule.objects.get(teacher=teacher)
    return render(request, 'teacher_page.html', {'teacher': teacher, 'subjects': subjects_list})


def teacher_profile(request):
    teacher_id = request.session.get('id')
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    teacher_image = get_object_or_404(CustomUser, id=teacher_id).image
    teacher_image_url = teacher_image.url
    default_image_url = '/media/user_images/default.png'

    # Check if teacher_image exists and the file exists on the server
    if not (teacher_image and os.path.exists(teacher_image.path)):
        teacher_image_url = default_image_url

    subjects_list = teacher.subjects.split(',')
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            # Get the cleaned data
            cleaned_data = form.cleaned_data

            image_data = request.POST.get('image')
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            user = request.user
            image = ContentFile(base64.b64decode(imgstr), name=f"""teacher_{user.get_username()}.{ext}""")
            user.image = image
            user.save()

            # Save the rest of the data to Teacher
            teacher_data = cleaned_data.copy()
            teacher_data['teacher_id'] = user.id
            Teacher.objects.update_or_create(
                teacher_id=user.id,
                defaults=teacher_data
            )
            return redirect('dashboard')
        else:
            return render(request, 'teacher_profile.html', {'subjects': subjects_list, 'form': form})
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'teacher_profile.html',
                  {'subjects': subjects_list, 'form': form, 'teacher_image_url': teacher_image_url})


def teacher_schedule(request):
    teacher_id = request.session.get('id')
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)

    # Try to get the existing schedule or initialize to None
    try:
        schedule = TeacherSchedule.objects.get(teacher=teacher)
    except TeacherSchedule.DoesNotExist:
        schedule = TeacherSchedule()
        schedule.teacher = teacher

    if request.method == 'POST':
        # Get the slots data from the hidden input field
        slots_data = request.POST.get('slots')
        slots = json.loads(slots_data)
        schedule.slots = slots

        schedule.save()
        return redirect('dashboard')

    else:
        # Prepare the existing slots for rendering in the template
        slots_json = json.dumps(schedule.slots) if schedule else '[]'
        return render(request, 'teacher_schedule.html', {'schedule': schedule, 'slots_json': slots_json})
