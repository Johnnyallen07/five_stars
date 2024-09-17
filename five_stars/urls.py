from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('purchase/', views.purchase, name='purchase'),
    path('', views.home_page, name='index'),
    path('', include('learning.urls')),
]
