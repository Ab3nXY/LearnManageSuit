from django.urls import path

from . import views
from calendarapp.views import SettingsView
app_name = "calendarapp"


urlpatterns = [
    path('calendar/', views.CalendarViewNew.as_view(), name='calendar'), 
    path('calendar/<int:staff_id>/', views.CalendarViewNew.as_view(), name='calendar_admin'),
    path("calendars/", views.CalendarView.as_view(), name="calendars"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path("event/new/", views.create_event, name="event_new"),
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    path("add_eventmember/<int:event_id>", views.add_eventmember, name="add_eventmember"),
    path("event/<int:pk>/remove",views.EventMemberDeleteView.as_view(),name="remove_event"),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path("running-event-list/",views.RunningEventsListView.as_view(),name="running_events"),
    path('settings/', SettingsView.as_view(), name='settings'),
]
