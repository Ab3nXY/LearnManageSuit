from django.views.generic import ListView
from calendarapp.models import Event, EventMember

class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Admins see all events
            return Event.objects.all()  # Retrieve all events for superusers
        elif user.role == "student":
            return Event.objects.filter(user=user)
        else:
            # Non-admins see their own events and events where they are members
            user_event_ids = EventMember.objects.filter(user=user).values_list('event_id', flat=True)
            return Event.objects.filter(id__in=user_event_ids)

class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Admins see all events
            return Event.objects.all()
        elif user.role == "student":
            return Event.objects.filter(is_active=True, user=user)
        else:
            # Non-admins see their own running events and events where they are members
            user_event_ids = EventMember.objects.filter(user=user).values_list('event_id', flat=True)
            user_events = Event.objects.filter(id__in=user_event_ids)
            return user_events.filter(is_active=True)  # Assuming you have a field is_running to indicate running events
