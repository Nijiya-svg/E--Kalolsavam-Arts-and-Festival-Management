from django import forms

from .models import Score


class ScoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Score
        fields = ("marks", "remarks")
        widgets = {
            "remarks": forms.Textarea(attrs={"rows": 3}),
        }
