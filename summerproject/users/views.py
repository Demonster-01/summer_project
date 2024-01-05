from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .models import User, Profile, Theater
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.decorators.csrf import csrf_protect

from django import forms


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Create a registration request object (not a user yet)
            form.save()
            # Notify the admin for approval (you can send an email or use other methods)
            messages.success(request, 'Your registration request has been submitted for admin approval.')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def search(request):
    # profiles=Profile.objects.all()
    query = request.GET['query']
    profiles = Profile.objects.filter(user__email__icontains=query)
    params = {'profiles': profiles}
    print("hi")
    return render(request, 'users/search.html', params)


def clean_email(self):
    data = self.cleaned_data['email']
    if User.objects.filter(email=data).exists():
        raise forms.ValidationError("this email is already used.")
    return data


class RegistrationrequestsView(ListView):
    model = Profile  # Use the capitalized model name
    template_name = 'users/user_request.html'
    context_object_name = "registration_requests"  # Update the context object name

    def get_queryset(self):
        return Profile.objects.filter(is_approved="false")


from .models import Profile


def approve_registration(request, request_id):
    try:
        # Retrieve the registration request
        registration_request = Profile.objects.get(id=request_id)
        registration_request.is_approved = True  # Assuming you have a field named 'is_approved'
        registration_request.save()

        messages.success(request, f'Registration request for {registration_request.user.username} has been approved.')
    except Profile.DoesNotExist:
        messages.error(request, 'Registration request not found.')

    return redirect('registration_requests')


def reject_registration(request, request_id):
    try:
        # Retrieve the registration request
        registration_request = Profile.objects.get(id=request_id)
        registration_request.delete()

        messages.warning(request, f'Registration request for {registration_request.user.username} has been rejected.')
    except Profile.DoesNotExist:
        messages.error(request, 'Registration request not found.')

    return redirect('registration_requests')


from django.contrib.auth import authenticate, login as auth_login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            # Check if the user's profile is approved
            profile = user.profile  # Assuming you have a one-to-one relationship between User and Profile
            if profile.is_approved.lower() == 'true':
                auth_login(request, user)
                return redirect("/")
            else:
                messages.error(request, 'Your account is not approved yet.')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'users/login.html')