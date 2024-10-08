from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Teacher, TeacherSchedule, TeacherDisplay


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_name', 'first_name', 'last_name', 'email', 'school')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('school',)
    ordering = ('last_name', 'first_name')

    # Optional: Customizing form layout
    fieldsets = (
        (None, {
            'fields': ('teacher_name', 'first_name', 'last_name', 'email', 'school')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('subjects', 'introduction'),
        }),
    )
    # Optional: Customizing the form used in the admin interface
    # form = TeacherForm


# Register the Teacher model with the admin site
admin.site.register(Teacher, TeacherAdmin)


class TeacherScheduleAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'available_slots')


admin.site.register(TeacherSchedule, TeacherScheduleAdmin)


class TeacherDisplayAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'brief_subjects')


admin.site.register(TeacherDisplay, TeacherDisplayAdmin)
