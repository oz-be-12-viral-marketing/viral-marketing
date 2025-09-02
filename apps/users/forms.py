from allauth.account.forms import SignupForm  # Import allauth's SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    name = forms.CharField(
        max_length=50,
        label="이름",
        widget=forms.TextInput(attrs={"placeholder": "이름을 입력하세요", "class": "form-control"}),
    )
    nickname = forms.CharField(
        max_length=25,
        label="닉네임",
        widget=forms.TextInput(attrs={"placeholder": "사용할 닉네임을 입력하세요", "class": "form-control"}),
    )
    phone_number = forms.CharField(
        max_length=20,
        label="전화번호",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "전화번호 (선택)", "class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        # Style the fields inherited from allauth's base SignupForm
        self.fields["email"].label = "이메일"
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "이메일 주소"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "비밀번호"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "비밀번호 확인"})

    def signup(self, request, user):
        user.name = self.cleaned_data["name"]
        user.nickname = self.cleaned_data["nickname"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.save()
        return user
