from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_id>/', views.course_access, name='course'),
    path('course/<int:course_id>/material', views.material_page, name='course_material'),
    path('course/<int:course_id>/upload', views.upload_page, name='upload'),
    path('course/<int:course_id>/info', views.course_info, name='course_info'),
    # one is editing data, and the other is adding post
    path('manage_post/<int:course_id>/<int:post_id>', views.manage_post, name='manage-post'),
    path('add_post/<int:course_id>', views.add_post, name='add-post'),

    path('delete_post', views.delete_post, name='delete-post'),
    path('save_post', views.save_post, name='save-post'),
]
