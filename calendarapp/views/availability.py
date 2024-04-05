from django.shortcuts import render, redirect
from calendarapp.forms import AvailabilityForm
from accounts.models import User

def set_availability(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours_range = range(24)
    
    # Retrieve availability data for the current user
    availability = None
    try:
        availability = request.user.availability  # Assuming availability is related to the user
    except User.DoesNotExist:
        pass

    if request.method == 'POST':
        form = AvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            # Save availability information to the database
            availability = form.save(commit=False)
            availability.user = request.user
            availability.save()
            return redirect("calendarapp:calendar")  # Redirect to a success page
    else:
        form = AvailabilityForm(instance=availability)  # Prefill form with existing data

    return render(request, "calendarapp/set_availability.html", {'form': form, 'days': days,'hours_range': hours_range})
