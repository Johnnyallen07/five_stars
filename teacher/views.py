from django.shortcuts import get_object_or_404, render

from five_stars.models import CustomUser
from teacher.models import Teacher


def teacher_page(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    return render(request, 'teacher_page.html', {'teacher': teacher})


def teacher_profile(request):
    teacher_id = request.session.get('teacher_id')
    teacher = get_object_or_404(CustomUser, id=teacher_id)
    return render(request, 'teacher_profile.html', {'teacher': teacher})
