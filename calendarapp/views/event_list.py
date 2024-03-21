from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from calendarapp.models import Event

class AllEventsListView(LoginRequiredMixin, ListView):
    """ All event list views """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Admins see all events
            return Event.objects.all()
        else:
            # Non-admins see only their own events
            return Event.objects.filter(created_by=user)


class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        user = self.request.user
        running_events = Event.objects.filter(is_running=True)  # Replace with your filter logic
        if user.is_superuser:
            # Admins see all running events
            return running_events
        else:
            # Non-admins see only their own running events
            return running_events.filter(created_by=user)

    def test_func(self):
        # Allow access to the view only if the user is authenticated
        return self.request.user.is_authenticated
