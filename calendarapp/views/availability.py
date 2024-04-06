from django.shortcuts import render, redirect
from calendarapp.forms import AvailabilityForm
from accounts.models import User

def set_availability(request):
    # Define the days of the week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Define the hours range in a 24-hour format
    hours_range = range(24)
    
    # Initialize availability data with default values
    availability_data = {
        'available_days': ','.join(days),  # Initially set all days as available
        'start_time': '00',  # Default start time (hour only)
        'end_time': '23'     # Default end time (hour only)
    }

    # Retrieve availability data for the current user if available
    try:
        user = request.user
        availability_data['available_days'] = getattr(user, 'available_days', availability_data['available_days'])
        availability_data['start_time'] = getattr(user, 'start_time', availability_data['start_time'])
        availability_data['end_time'] = getattr(user, 'end_time', availability_data['end_time'])
    except User.DoesNotExist:
        pass

    if request.method == 'POST':
        form = AvailabilityForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the form data
            return redirect("calendarapp:calendar")  # Redirect to a success page
    else:
        form = AvailabilityForm(initial=availability_data)

    return render(request, "calendarapp/set_availability.html", {'form': form, 'days': days,'hours_range': hours_range})
