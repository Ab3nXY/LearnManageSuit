# cal/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from calendarapp.models import EventMember, Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm, SettingsForm
from django.contrib.auth.models import User
from accounts.models import User
from django.views import View
from django.shortcuts import get_object_or_404
from django import forms

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Event
    template_name = "calendars.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


@login_required
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("calendarapp:calendar"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"
    success_url = reverse_lazy("calendarapp:calendar")  # Redirect to the event list page after successful update

    def get_object(self, queryset=None):
        # Get the event object based on the URL parameter
        return Event.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        # Save the form with the updated data
        form.save()
        return super().form_valid(form)



@login_required
def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)



def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data["user"]
                EventMember.objects.create(event=event, user=user)
                return redirect("calendarapp:calendar")
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")

class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, staff_id=None, *args, **kwargs):
            if User.is_superuser:
                # Admin view: Show all events and staff members
                if staff_id:
                    # Show events for specific staff member (if staff_id provided)
                    events = Event.objects.filter(user_id=staff_id).select_related('user__profile')
                else:
                    # Show all events for current user
                    events = Event.objects.get_all_events(user=request.user).select_related('user__profile')
                events_month = Event.objects.get_running_events(user=request.user)  # Assuming this filters events for the current month

                event_list = []
                for event in events:
                    event_list.append({
                        "id": event.id,
                        "title": event.title,
                        "start": event.start_time.strftime("%b %d, %Y at %H:%M"),
                        "end": event.end_time.strftime("%b %d, %Y at %H:%M"),
                        "description": event.description,
                        "creator_border_color": event.user.profile.border_color,  # New field
                    })

                staff_members = User.objects.filter(role__in=["tutor", "guidance"]).select_related('profile')

                
                context = {
                    # "id": event.id,
                    "form": self.form_class(),
                    "events": event_list,
                    "events_month": events_month,
                    "staff_members": staff_members,
                }
                return render(request, self.template_name, context)

            else:
                # Regular user view: Show only their events
                events = Event.objects.get_all_events(user=request.user).select_related('user__profile')
                events_month = Event.objects.get_running_events(user=request.user)  # Assuming this filters events for the current month

                event_list = []
                for event in events:
                    event_list.append({
                        "id": event.id,
                        "title": event.title,
                        "start": event.start_time.strftime("%b %d, %Y at %H:%M"),
                        "end": event.end_time.strftime("%b %d, %Y at %H:%M"),
                        "description": event.description,
                        "creator_border_color": event.user.profile.border_color,  # New field

                    })

                context = {
                    "form": self.form_class(),
                    "events": event_list,
                    "events_month": events_month,
                }
                return render(request, self.template_name, context) 


        
    def post(self, request, *args, **kwargs):
        # Handle form submission logic here
        forms = self.form_class(request.POST)
        if forms.is_valid():
            # Process the form data and create the event
            title = forms.cleaned_data["title"]
            description = forms.cleaned_data["description"]
            start_time = forms.cleaned_data["start_time"]
            end_time = forms.cleaned_data["end_time"]
            Event.objects.create(
                user=request.user,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
            )
            return redirect("calendarapp:calendar")  # Redirect to calendar view
        else:
            # Handle form validation errors
            return render(request, self.template_name, {"form": forms})

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_week(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=7)
        next.end_time += timedelta(days=7)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_day(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=1)
        next.end_time += timedelta(days=1)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)
    
class SettingsView(LoginRequiredMixin, View):
    login_url = 'accounts:signin'
    template_name = 'calendarapp/settings.html'  

    def get(self, request, *args, **kwargs):
        form = SettingsForm()  # Initialize the set availability form
        # Add any additional logic here, such as fetching initial data for the form
        context = {'form': form}
        return render(request, self.template_name, context)
    

