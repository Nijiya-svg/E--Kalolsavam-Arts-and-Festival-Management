from django.conf import settings
from django.db import models

from events.models import Event, Participation


class JudgeAssignment(models.Model):
    judge = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="judge_assignments",
        limit_choices_to={"role": "judge"},
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="judge_assignments")

    class Meta:
        unique_together = ("judge", "event")

    def __str__(self):
        return f"{self.judge.email} -> {self.event.name}"


class Score(models.Model):
    judge = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scores_given",
        limit_choices_to={"role": "judge"},
    )
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name="scores")
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("judge", "participation")

    def __str__(self):
        return f"{self.judge.email} scored {self.participation}"
