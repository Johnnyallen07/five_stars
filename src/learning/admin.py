from django.contrib import admin
from .models import Topic, Subtopic, Course, MaterialPost


class SubtopicInline(admin.TabularInline):
    model = Subtopic
    extra = 1  # Shows one extra field for convenience


class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "course"]
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
    list_display = ("title", "image_url")
    search_fields = ("title",)


admin.site.register(MaterialPost)
