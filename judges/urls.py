from django.urls import path

from .views import JudgeAssignedEventsView, JudgeScoreUpdateView

app_name = "judges"

urlpatterns = [
    path("judge/events/", JudgeAssignedEventsView.as_view(), name="judge-events"),
    path("judge/score/<int:pk>/", JudgeScoreUpdateView.as_view(), name="judge-score"),
]
