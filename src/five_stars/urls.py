from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path(
        "post_register_teacher/",
        views.post_register_teacher_view,
        name="post_register_teacher",
    ),
    path(
        "post_register_student/",
        views.post_register_student_view,
        name="post_register_student",
    ),
    path("teacher-register/", views.teacher_register_view, name="teacher-register"),
    path(
        "teacher-register/profile",
        views.teacher_register_profile,
        name="teacher-register-profile",
    ),
    path("purchase/", views.purchase_view, name="purchase"),
    path("home/", views.home_view, name="home"),
    path("dashboard/", views.teacher_dashboard_view, name="dashboard"),
    path("", views.index_page_view, name="index"),
    path("", include("learning.urls")),
    path("", include("teacher.urls")),
    path("", include("user.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
