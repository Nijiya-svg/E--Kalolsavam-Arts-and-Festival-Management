from django.contrib import admin

from .models import JudgeAssignment, Score


@admin.register(JudgeAssignment)
class JudgeAssignmentAdmin(admin.ModelAdmin):
    list_display = ("judge", "event")
    search_fields = ("judge__email", "event__name")


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("judge", "participation", "marks", "updated_at")
    list_filter = ("participation__event",)
    search_fields = ("judge__email", "participation__student__email", "participation__event__name")
