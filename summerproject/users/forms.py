from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # we can live EmailField(required=True) for true
    first_name = forms.CharField()
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'password1', 'password2']


# class UserUpdateForm(forms.ModelForm):
#     email=forms.EmailField()
#     class Meta:
#         model = User
#         fields=['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']




# @login_required
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # fields = ['role','theater_name']
        fields=['role']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update({'class': 'form-control'})

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Profile'
        return context
    def test_func(self):
        user_profile = self.get_object()
        return self.request.user.is_authenticated and (self.request.user.is_superuser or user_profile.role == 'admin')

