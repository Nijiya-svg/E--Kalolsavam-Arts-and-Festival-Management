from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, UpdateView

from accounts.mixins import RoleRequiredMixin
from events.models import Participation

from .forms import ScoreForm
from .models import JudgeAssignment, Score


class JudgeAssignedEventsView(RoleRequiredMixin, ListView):
    allowed_roles = ("judge",)
    template_name = "judges/judge_events.html"
    context_object_name = "assignments"

    def get_queryset(self):
        return JudgeAssignment.objects.filter(judge=self.request.user).select_related("event")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_ids = [assignment.event_id for assignment in context["assignments"]]
        context["participations"] = (
            Participation.objects.filter(event_id__in=event_ids)
            .select_related("student", "event")
            .order_by("event__date", "event__name")
        )
        return context


class JudgeScoreUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ("judge",)
    template_name = "judges/judge_score_form.html"
    form_class = ScoreForm
    model = Score
    context_object_name = "score"

    def dispatch(self, request, *args, **kwargs):
        self.participation = get_object_or_404(
            Participation.objects.select_related("event", "student"),
            pk=self.kwargs["pk"],
        )
        assigned = JudgeAssignment.objects.filter(
            judge=request.user,
            event=self.participation.event,
        ).exists()
        if not assigned:
            messages.error(request, "You are not assigned to this event.")
            return redirect("judges:judge-events")

        self.score, _ = Score.objects.get_or_create(
            judge=request.user,
            participation=self.participation,
            defaults={"marks": 0, "remarks": ""},
        )
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.score

    def form_valid(self, form):
        messages.success(self.request, "Score saved successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participation"] = self.participation
        return context
