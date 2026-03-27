from django.urls import path

from .views import VolunteerDutyListView

app_name = "volunteers"

urlpatterns = [
    path("volunteer/duty/", VolunteerDutyListView.as_view(), name="volunteer-duty"),
]
