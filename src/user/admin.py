from django.contrib import admin

from user.models import UserSchedule


# Register your models here.
class UserScheduleAdmin(admin.ModelAdmin):
    list_display = ("user", "reserved_slots", "completed_slots", "missed_slots")


admin.site.register(UserSchedule, UserScheduleAdmin)
