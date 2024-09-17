from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('learn/', views.learn_view, name='learn'),
    path('purchase/', views.purchase, name='purchase'),
    path('course/<int:course_id>/', views.course_access, name='course'),
    path('', views.home_page, name='index')
]
