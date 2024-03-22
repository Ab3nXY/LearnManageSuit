from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from accounts.models import User
from allauth.account.forms import SignupForm

class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

class MyCustomSignUpForm(SignupForm):
    first_name = forms.CharField(
        label="First Name",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]
        widgets = {"email": forms.EmailInput(attrs={"class": "form-control"})}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password didn't match!")
        return password2

    def save(self, request):
        user = super(MyCustomSignUpForm, self).save(request)
        user.set_password(self.cleaned_data["password1"])
        return user

class UserProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control-file"}))
    border_color = forms.CharField(max_length=20)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'image', 'border_color']

