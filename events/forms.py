from django import forms

from .models import Participation


class ParticipationStatusForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ("status",)
