from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm


# Load page for user registration
def register(request):
    if request.method == 'POST':
        # Creates the form with the data from the request.POST
        form = UserRegistrationForm(request.POST)

        # Checks for valid usernames, matching passwords
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Thanks {username}, your account has been created. You are now able to log in!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'title': 'register', 'form': form})


# View of profile, decorator makes it so user must be logged in to view this page.
@login_required
def profile(request):

    if request.method == 'POST':
        # Giving instances lets form fields be filled in with current values.
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Thanks {request.user.username}, your account has been updated.')

            # Use redirect here to avoid "are you sure you want to resend form" prompt
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'title': 'profile',
               'u_form': u_form,
               'p_form': p_form}

    return render(request, 'users/profile.html', context)
