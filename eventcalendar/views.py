from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from calendarapp.models import Event
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
        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        if request.user.is_superuser:
          latest_events = Event.objects.order_by("-id")[:10]
        else:
          latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]

        for event in latest_events:
            members = event.events.all()
        # Get student and tutor counts
        total_students = get_student_count(user=request.user)
        total_tutors = get_tutor_count(user=request.user)

        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
            "total_students": total_students,
            "total_tutors": total_tutors,
        }
        return render(request, self.template_name, context)
