from django.contrib import admin

from .models import VolunteerAssignment


@admin.register(VolunteerAssignment)
class VolunteerAssignmentAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "event")
    search_fields = ("volunteer__email", "event__name")
