from django import forms
from allauth.account.forms import SignupForm # Import allauth's SignupForm

class CustomSignupForm(SignupForm): # Inherit from allauth's SignupForm
    name = forms.CharField(max_length=50, label='Name')
    nickname = forms.CharField(max_length=25, label='Nickname')
    phone_number = forms.CharField(max_length=20, label='Phone Number', required=False) # Added phone_number

    def signup(self, request, user):
        user.name = self.cleaned_data['name']
        user.nickname = self.cleaned_data['nickname']
        user.phone_number = self.cleaned_data['phone_number'] # Save phone_number
        user.save()
        return user
