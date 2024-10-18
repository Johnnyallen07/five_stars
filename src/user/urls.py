from django.urls import path
from . import views

urlpatterns = [
    path('user-profile/', views.user_profile, name='user-profile'),
    path('my-learning/', views.user_dashboard, name='user-dashboard')
]
