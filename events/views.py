from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View

from accounts.mixins import RoleRequiredMixin

from .models import Event, Participation


class StudentEventListView(RoleRequiredMixin, ListView):
    allowed_roles = ("student",)
    model = Event
    template_name = "events/student_events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.annotate(registered_count=Count("participations")).order_by("date", "name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registered_event_ids"] = set(
            Participation.objects.filter(student=self.request.user).values_list("event_id", flat=True)
        )
        return context


class RegisterEventView(RoleRequiredMixin, View):
    allowed_roles = ("student",)

    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs["pk"])

        if Participation.objects.filter(student=request.user, event=event).exists():
            messages.warning(request, "You are already registered for this event.")
            return redirect("events:student-events")

        if event.participations.count() >= event.max_participants:
            messages.error(request, "Registration closed. Maximum participants reached.")
            return redirect("events:student-events")

        Participation.objects.create(student=request.user, event=event)
        messages.success(request, "Event registration successful.")
        return redirect("events:student-events")


class MyParticipationListView(RoleRequiredMixin, ListView):
    allowed_roles = ("student",)
    template_name = "events/student_my.html"
    context_object_name = "participations"

    def get_queryset(self):
        return (
            Participation.objects.filter(student=self.request.user)
            .select_related("event")
            .prefetch_related("scores__judge")
        )
