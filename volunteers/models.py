from django.conf import settings
from django.db import models

from events.models import Event


class VolunteerAssignment(models.Model):
    volunteer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="volunteer_assignments",
        limit_choices_to={"role": "volunteer"},
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="volunteer_assignments")
    duty_description = models.TextField()

    class Meta:
        unique_together = ("volunteer", "event")

    def __str__(self):
        return f"{self.volunteer.email} -> {self.event.name}"
