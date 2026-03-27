from django.contrib import admin

from .models import Event, Participation


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "date", "venue", "max_participants")
    list_filter = ("category", "date")
    search_fields = ("name", "venue", "category")


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("student", "event", "status", "created_at")
    list_filter = ("status", "event")
    search_fields = ("student__email", "event__name")
