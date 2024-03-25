from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileUpdateForm

@login_required
def update_profile(request):
    try:
        profile_updated = request.session['profile_updated']
    except KeyError:
        profile_updated = False

    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user = user_form.save(commit=False)  # Don't commit yet
            if request.FILES.get('image'):
                user.profile.image = request.FILES['image']  # Update profile image
            user.save()
            request.session['profile_updated'] = True  # Set a session variable
            return redirect('accounts:profile')
    else:
        user_form = UserProfileUpdateForm(instance=request.user)

    context = {'user_form': user_form, 'profile_updated': profile_updated}
    return render(request, 'accounts/profile.html', context)
