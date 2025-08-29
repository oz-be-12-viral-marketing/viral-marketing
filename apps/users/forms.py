from django import forms

class CustomSignupForm(forms.Form):
    name = forms.CharField(max_length=50, label='Name')
    nickname = forms.CharField(max_length=25, label='Nickname')

    def signup(self, request, user):
        user.name = self.cleaned_data['name']
        user.nickname = self.cleaned_data['nickname']
        user.save()
        return user
