from django.forms import ModelForm, formset_factory, DateInput, ValidationError
from calendarapp.models import Event, EventMember
from django import forms

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

    def clean(self):
        cleaned_data = super().clean()
        event = self.instance.event  # Access the associated event instance
        if event:
            # Check if the user is already a member of this event
            if EventMember.objects.filter(event=event, user=cleaned_data['user']).exists():
                raise ValidationError('This user is already a member of this event.')
        return cleaned_data


class SettingsForm(forms.Form):
    start_time = forms.DateTimeField(label='Start Time')
    end_time = forms.DateTimeField(label='End Time')
