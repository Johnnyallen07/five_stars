from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_id>/', views.course_access, name='course'),
    path('course/<int:course_id>/material', views.material_page, name='course_material')
]
