from django import forms
from django.contrib.auth import authenticate
from apps.users.models import CustomUser
from apps.accounts.models import Account # Import Account model
from apps.accounts.choices import BANK_CODES, ACCOUNT_TYPE, CURRENCIES # Import choices
from apps.transaction_history.models import TransactionHistory # Import TransactionHistory model
from apps.transaction_history.choices import TRANSACTION_TYPE, TRANSACTION_METHOD # Import choices

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
    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '계좌번호'}), label='계좌번호')
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE, widget=forms.Select(attrs={'class': 'form-control'}), label='유형')
    currency = forms.ChoiceField(choices=CURRENCIES, widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Account
        fields = ['bank_code', 'account_number', 'account_type', 'currency'] # Added account_number
        # balance, user are handled by the view/model
        widgets = {
            # No need for balance, user here
        }

    def save(self, commit=True, user=None):
        account = super().save(commit=False)
        if user:
            account.user = user
        # account_number is now handled by the form
        # balance will be set in the view or model's save method/signal
        if commit:
            account.save()
        return account

class TransactionForm(forms.ModelForm):
    # account field should be a ChoiceField to select from user's accounts
    # We'll populate choices in the view
    account = forms.ModelChoiceField(
        queryset=Account.objects.none(), # Will be set in __init__
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='계좌'
    )
    transaction_type = forms.ChoiceField(
        choices=TRANSACTION_TYPE,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='유형'
    )
    transaction_method = forms.ChoiceField(
        choices=TRANSACTION_METHOD,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='거래 방식'
    )
    
    class Meta:
        model = TransactionHistory
        fields = ['account', 'transaction_type', 'amount', 'transaction_detail', 'transaction_method']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '금액'}),
            'transaction_detail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '상세 내용 (선택 사항)'}),
        }
        labels = {
            'amount': '금액',
            'transaction_detail': '상세 내용',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        amount = cleaned_data.get('amount')
        account = cleaned_data.get('account')

        if transaction_type == 'WITHDRAW' and account and amount:
            if account.balance < amount:
                raise forms.ValidationError('잔액이 부족합니다.')
        return cleaned_data

    def save(self, commit=True, user=None):
        transaction = super().save(commit=False)
        # The account balance update logic will be handled in the view for now,
        # similar to how it's done in the API's perform_create.
        # This form's save method will just create the transaction object.
        if commit:
            transaction.save()
        return transaction

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'nickname', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }