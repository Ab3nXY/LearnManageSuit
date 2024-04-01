from django.db import models
from accounts.models import User  
from django.core.exceptions import ValidationError
from calendarapp.models import Event, EventAbstract

class EventMember(EventAbstract):
    """ Event member model """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_members"
    )

    class Meta:
        unique_together = ["event", "user"]

    def __str__(self):
        return str(self.user)
    
    @property
    def border_color(self):
        return self.user.profile.border_color

    def clean(self):
        # Check if user is staff
        if not self.user.is_staff:
            raise ValidationError('Event member must be a staff user.')
        super().clean()  # Call parent clean method
