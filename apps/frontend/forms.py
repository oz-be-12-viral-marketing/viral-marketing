from django import forms
from django.contrib.auth import authenticate
from apps.users.models import CustomUser
from apps.accounts.models import Account # Import Account model
from apps.accounts.choices import BANK_CODES, ACCOUNT_TYPE, CURRENCIES # Import choices

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일 주소'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('이메일 또는 비밀번호가 올바르지 않습니다.')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('비활성화된 계정입니다.')
        return self.cleaned_data

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호 확인'}), label='비밀번호 확인')

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'nickname', 'phone_number')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일 주소'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '닉네임'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '전화번호'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True # Frontend registration should activate user directly
        if commit:
            user.save()
        return user

class AccountForm(forms.ModelForm):
    bank_code = forms.ChoiceField(choices=BANK_CODES, widget=forms.Select(attrs={'class': 'form-select'}))
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE, widget=forms.Select(attrs={'class': 'form-select'}))
    currency = forms.ChoiceField(choices=CURRENCIES, widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Account
        fields = ['bank_code', 'account_type', 'currency'] # Only these fields are user-inputted
        # account_number, balance, user are handled by the view/model
        widgets = {
            # No need for account_number, balance, user here
        }

    def save(self, commit=True, user=None):
        account = super().save(commit=False)
        if user:
            account.user = user
        # account_number and balance will be set in the view or model's save method/signal
        if commit:
            account.save()
        return account