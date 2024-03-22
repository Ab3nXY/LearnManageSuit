from django.views.generic import ListView
from calendarapp.models import Event

class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Admins see all events
            return Event.objects.all()  # Retrieve all events for superusers
         # Non-admins see only their own events
        return Event.objects.get_all_events(user=user)

class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Admins see all events
            return Event.objects.all()
        # Non-admins see only their own events
        return Event.objects.get_running_events(user=user)
