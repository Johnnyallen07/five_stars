from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('course/<int:course_id>/', views.course_access, name='course'),
]
