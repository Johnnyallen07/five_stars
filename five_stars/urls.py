from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('teacher-register/', views.teacher_register_view, name='teacher-register'),
    path('purchase/', views.purchase, name='purchase'),
    path('home/', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.home_page, name='index'),
    path('', include('learning.urls')),

    path('', include('teacher.urls')),
]
