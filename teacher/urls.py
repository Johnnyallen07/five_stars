from django.urls import path
from . import views

urlpatterns = [
    path('teacher/<int:teacher_id>/', views.teacher_page, name='teacher'),
    path('teacher-profile/', views.teacher_profile, name='teacher-profile')
]
