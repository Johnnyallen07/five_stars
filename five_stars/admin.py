from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Topic, Subtopic, Course, CustomUser
from django.contrib.auth.models import Group

admin.site.unregister(Group)


class SubtopicInline(admin.TabularInline):
    model = Subtopic
    extra = 1  # Shows one extra field for convenience


class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    inlines = [SubtopicInline]
    #
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     if obj:  # When editing an existing topic
    #         form.base_fields['course'].queryset = Course.objects.filter(id=obj.course.course_id)
    #     return form


admin.site.register(Topic, TopicAdmin)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_url')
    search_fields = ('title',)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Define which fields are displayed on the user detail page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'subscriptions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = UserAdmin.filter_horizontal + ('subscriptions',)
    list_display = ('username', 'is_staff')  #


admin.site.register(CustomUser, CustomUserAdmin)
