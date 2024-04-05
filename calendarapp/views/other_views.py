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
from calendarapp.forms import EventForm, AddMemberForm
from django.contrib.auth.models import User
from accounts.models import User
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

def create_event_and_add_member(request, event_form, add_member_form_class, event_instance=None):
    if event_form.is_valid():
        if event_instance:
            # If an event instance is provided, update the existing event
            event = event_form.save()
        else:
            # Otherwise, create a new event
            event = event_form.save(commit=False)
            event.user = request.user
            event.save()

        # Get the selected user from the add member form
        add_member_form = add_member_form_class(request.POST)
        if add_member_form.is_valid():
            user = add_member_form.cleaned_data["user"]

            try:
                # Check if there's an existing event member
                existing_member = EventMember.objects.get(event=event)
                existing_member.user = user  # Replace existing member with the selected user
                existing_member.save()
            except ObjectDoesNotExist:
                # No existing event member found, create a new one
                EventMember.objects.create(event=event, user=user)

            return event, None  # No add_member_form errors

    # If form validation fails or no user is selected, return None for event and add_member_form
    return None, None


# def get_date(req_day):
#     if req_day:
#         year, month = (int(x) for x in req_day.split("-"))
#         return date(year, month, day=1)
#     return datetime.today()


# def prev_month(d):
#     first = d.replace(day=1)
#     prev_month = first - timedelta(days=1)
#     month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
#     return month


# def next_month(d):
#     days_in_month = calendar.monthrange(d.year, d.month)[1]
#     last = d.replace(day=days_in_month)
#     next_month = last + timedelta(days=1)
#     month = "month=" + str(next_month.year) + "-" + str(next_month.month)
#     return month


# class CalendarView(LoginRequiredMixin, generic.ListView):
#     login_url = "accounts:signin"
#     model = Event
#     template_name = "calendars.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         d = get_date(self.request.GET.get("month", None))
#         cal = Calendar(d.year, d.month)
#         html_cal = cal.formatmonth(withyear=True)
#         context["calendar"] = mark_safe(html_cal)
#         context["prev_month"] = prev_month(d)
#         context["next_month"] = next_month(d)
#         return context


# @login_required
# def create_event(request):
#     event_form = EventForm(request.POST or None)

#     if request.POST and event_form.is_valid() and add_member_form.is_valid():
#         title = event_form.cleaned_data["title"]
#         description = event_form.cleaned_data["description"]
#         start_time = event_form.cleaned_data["start_time"]
#         end_time = event_form.cleaned_data["end_time"]

#         # Create event
#         event, created = Event.objects.get_or_create(
#             user=request.user,
#             title=title,
#             description=description,
#             start_time=start_time,
#             end_time=end_time,
#         )

#         return HttpResponseRedirect(reverse("calendarapp:calendar"))

#     return render(request, "event.html", {"event_form": event_form, "add_member_form": add_member_form})


class EventEdit(generic.UpdateView):
    form_class = EventForm
    template_name = "event.html"
    success_url = reverse_lazy("calendarapp:calendar")  # Redirect to the event list page after successful update
    add_member_form_class = AddMemberForm  # New attribute for member addition form

    def get_object(self, queryset=None):
        # Get the event object based on the URL parameter
        return Event.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()  # Retrieve the event object
        add_member_form = self.add_member_form_class()  # Pre-populate event field
        # Filter users with roles 'tutor' or 'guidance'
        tutors_and_guidance = User.objects.filter(Q(role="tutor") | Q(role="guidance"))
        context['add_member_form'] = add_member_form
        context['tutors_and_guidance'] = tutors_and_guidance  # Pass the filtered users to the template
        context['event'] = event  # Pass the event object to the context
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event_form = self.form_class(request.POST, instance=self.object)
        add_member_form = self.add_member_form_class(request.POST)

        event, add_member_form = create_event_and_add_member(request, event_form, self.add_member_form_class, event_instance=self.object)

        if event:
            return super().post(request, *args, **kwargs)  # Save the form with the updated data
        else:
            # Handle form validation errors
            return render(request, self.template_name, {"form": event_form, 'add_member_form': add_member_form})



# @login_required
# def event_details(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     eventmember = EventMember.objects.filter(event=event)
#     context = {"event": event, "eventmember": eventmember}
#     return render(request, "event-details.html", context)



# def add_eventmember(request, event_id):
#     event = Event.objects.get(id=event_id)

#     # Leverage the custom manager for filtered user choices
#     users = User.objects.filter(Q(role="tutor") | Q(role="guidance"))

#     if request.method == "POST":
#         add_member_form = AddMemberForm(request.POST, queryset=users)  # Pass filtered queryset
#         if add_member_form.is_valid():
#             user = add_member_form.cleaned_data["user"]
#             EventMember.objects.create(event=event, user=user)
#             return redirect("calendarapp:calendar")
#         else:
#             print("--------------Form is invalid!-----------------")

#     context = {"add_member_form": add_member_form, "event_id": event_id, "event_members": []}
#     return render(request, "add_member.html", context)

    


# class EventMemberDeleteView(generic.DeleteView):
#     model = EventMember
#     template_name = "event_delete.html"
#     success_url = reverse_lazy("calendarapp:calendar")

class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm
    add_member_form_class = AddMemberForm  # New attribute for member addition form

    def get(self, request, staff_id=None, *args, **kwargs):
            if request.user.is_superuser:
                if staff_id:
                    user = get_object_or_404(User, pk=staff_id)
                    event_ids = EventMember.objects.filter(user=user).values_list('event_id', flat=True)
                    events = Event.objects.filter(id__in=event_ids)
                else:
                    events = Event.objects.get_all_events(user=request.user)
            else:
                events = Event.objects.get_all_events(user=request.user)

            events_month = Event.objects.filter(user=request.user)  # Assuming this filters events for the current month
            

            event_list = []
            for event in events:
                event_list.append({
                    "id": event.id,
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M"),
                    "description": event.description,
                    "creator_border_color": event.user.profile.border_color  # New field
                })

            # Fetch events where the user is a member
            user_event_ids = EventMember.objects.filter(user=request.user).values_list('event_id', flat=True)
            user_events = Event.objects.filter(id__in=user_event_ids)
            for event in user_events:
                event_list.append({
                    "id": event.id,
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M"),
                    "description": event.description,
                    "creator_border_color": event.user.profile.border_color,  # New field
                })

            staff_members = User.objects.filter(role__in=["tutor", "guidance"])
            add_member_form = self.add_member_form_class()  # Pre-populate event field
            # Filter users with roles 'tutor' or 'guidance'
            tutors_and_guidance = User.objects.filter(Q(role="tutor") | Q(role="guidance"))

            context = {
                "form": self.form_class(),
                "events": event_list,
                "events_month": events_month,
                "staff_members": staff_members if request.user.is_superuser else None,
                'add_member_form':add_member_form,
                'tutors_and_guidance':tutors_and_guidance
            }
            return render(request, self.template_name, context)
        
    def post(self, request, *args, **kwargs):
        # Handle form submission logic here
        forms = self.form_class(request.POST)
        add_member_form = self.add_member_form_class(request.POST)

        event, add_member_form = create_event_and_add_member(request, forms, self.add_member_form_class)

        if event:
            return redirect("calendarapp:calendar")  # Redirect to calendar view
        else:
            # Handle form validation errors
            return render(request, self.template_name, {"form": forms, 'add_member_form': add_member_form})

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

# def next_week(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     if request.method == 'POST':
#         next = event
#         next.id = None
#         next.start_time += timedelta(days=7)
#         next.end_time += timedelta(days=7)
#         next.save()
#         return JsonResponse({'message': 'Sucess!'})
#     else:
#         return JsonResponse({'message': 'Error!'}, status=400)

# def next_day(request, event_id):

#     event = get_object_or_404(Event, id=event_id)
#     if request.method == 'POST':
#         next = event
#         next.id = None
#         next.start_time += timedelta(days=1)
#         next.end_time += timedelta(days=1)
#         next.save()
#         return JsonResponse({'message': 'Sucess!'})
#     else:
#         return JsonResponse({'message': 'Error!'}, status=400)
    
   

