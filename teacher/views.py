from django.shortcuts import get_object_or_404, render, redirect

from five_stars.models import CustomUser
from teacher.forms import TeacherForm
from teacher.models import Teacher


def teacher_page(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    subjects_list = teacher.subjects.split(',')  # Split the subjects
    return render(request, 'teacher_page.html', {'teacher': teacher, 'subjects': subjects_list})


def teacher_profile(request):
    teacher_id = request.session.get('teacher_id')
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    subjects_list = teacher.subjects.split(',')
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            # Optionally add a success message or redirect
            return redirect('dashboard')
        else:
            return render(request, 'teacher_profile.html', {'subjects': subjects_list, 'form': form})
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teacher_profile.html', {'subjects': subjects_list, 'form': form})
