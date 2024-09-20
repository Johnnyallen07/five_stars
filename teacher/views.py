from django.shortcuts import get_object_or_404, render

from five_stars.models import CustomUser
from teacher.forms import TeacherForm
from teacher.models import Teacher


def teacher_page(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    subjects_list = teacher.subjects.split(',')  # Split the subjects
    return render(request, 'teacher_page.html', {'teacher': teacher, 'subjects': subjects_list})


def teacher_profile(request):
    teacher_id = request.session.get('teacher_id')
    teacher = get_object_or_404(CustomUser, id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally add a success message or redirect
        else:
            # Pass the form with errors to the template
            return render(request, 'teacher_profile.html', {'teacher': teacher, 'form': form})
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teacher_profile.html', {'teacher': teacher, 'form': form})
