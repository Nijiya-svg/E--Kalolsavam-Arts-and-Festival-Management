from django.conf import settings
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    date = models.DateField()
    venue = models.CharField(max_length=200)
    max_participants = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("date", "name")

    def __str__(self):
        return self.name


class Participation(models.Model):
    STATUS_REGISTERED = "Registered"
    STATUS_COMPLETED = "Completed"

    STATUS_CHOICES = (
        (STATUS_REGISTERED, "Registered"),
        (STATUS_COMPLETED, "Completed"),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participations",
        limit_choices_to={"role": "student"},
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participations")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_REGISTERED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "event")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.student.email} - {self.event.name}"
