from django.forms import ModelForm, formset_factory, DateInput, ValidationError
from calendarapp.models import Event, EventMember
from django import forms
from accounts.models import User

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


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]

class AvailabilityForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['available_days', 'start_time', 'end_time']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.is_staff:
            # If the user is not staff, exclude the availability fields
            self.fields.pop('available_days')
            self.fields.pop('start_time')
            self.fields.pop('end_time')
        else:
            # Provide default values for availability fields
            self.fields['available_days'].initial = ''  # Provide default value for available_days
            self.fields['start_time'].initial = None  # Provide default value for start_time
            self.fields['end_time'].initial = None    # Provide default value for end_time
