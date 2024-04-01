from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from calendarapp.models import Event, EventMember
from accounts.models import User

def get_student_count(user):
  """
  Retrieves the number of users with the "student" role.
  """
  return User.objects.filter(role="student").count()

def get_tutor_count(user):
  """
  Retrieves the number of users with the "tutor" role.
  """
  return User.objects.filter(role="tutor").count()


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_superuser:
          #for a superuser view all events
          user_events = Event.objects
        elif user.role == 'student':
            # For students, only show events created by them
            user_events = Event.objects.filter(user=user)
        else:
            # For other users (e.g., staff or admins), show all events
            user_event_ids = EventMember.objects.filter(user=user).values_list('event_id', flat=True)
            user_events = Event.objects.filter(id__in=user_event_ids)

        # Fetch running events for the user
        running_events = user_events.filter(is_active=True)

        latest_events = user_events.order_by("-id")[:10]

        # Get student and tutor counts
        total_students = get_student_count(user=user)
        total_tutors = get_tutor_count(user=user)

        context = {
            "total_event": user_events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
            "total_students": total_students,
            "total_tutors": total_tutors,
        }
        return render(request, self.template_name, context)

