from django.forms import ModelForm, formset_factory, DateInput, ValidationError
from calendarapp.models import Event, EventMember
from django import forms
from django.forms.widgets import TextInput

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                    "rows": 2,
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"}, format="%Y-%m-%dT%H:%M"
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"}, format="%Y-%m-%dT%H:%M"
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)

        # Create a formset for adding multiple event members
        self.helper = formset_factory(AddMemberForm, extra=1)
        self.event_members = self.helper()

class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]
        labels = {'user': 'Tutor'}

class SettingsForm(forms.Form):
    start_time = forms.DateTimeField(label='Start Time')
    end_time = forms.DateTimeField(label='End Time')
