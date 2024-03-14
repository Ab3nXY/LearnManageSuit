from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileUpdateForm

@login_required
def update_profile(request):
    user_form = UserProfileUpdateForm(instance=request.user)  # Create empty form for GET
    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user = user_form.save(commit=False)  # Don't commit yet
            if request.FILES.get('image'):
                user.image = request.FILES['image']
            user.save()
            request.session['profile_updated'] = True  # Set a session variable
            return redirect('accounts:profile')
    context = {'user_form': user_form, 'profile_updated': request.session.pop('profile_updated', False)}
    return render(request, 'accounts/profile.html', context)

