from django.views.generic import ListView

from accounts.mixins import RoleRequiredMixin

from .models import VolunteerAssignment


class VolunteerDutyListView(RoleRequiredMixin, ListView):
    allowed_roles = ("volunteer",)
    template_name = "volunteers/volunteer_duty.html"
    context_object_name = "duties"

    def get_queryset(self):
        return VolunteerAssignment.objects.filter(volunteer=self.request.user).select_related("event")
