from django.urls import path

from .views import MyParticipationListView, RegisterEventView, StudentEventListView

app_name = "events"

urlpatterns = [
    path("student/events/", StudentEventListView.as_view(), name="student-events"),
    path("student/events/register/<int:pk>/", RegisterEventView.as_view(), name="register-event"),
    path("student/my/", MyParticipationListView.as_view(), name="student-my"),
]
