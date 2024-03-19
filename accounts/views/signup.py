from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import SignUpForm

from verify_email.email_handler import send_verification_email


class SignUpView(View):
    """User registration view with email verification"""

    template_name = "accounts/signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            inactive_user = send_verification_email(request, forms)
            return redirect("accounts:signup_success")
        context = {"form": forms}
        return render(request, self.template_name, context)


def signup_success(request):
    return render(request, 'accounts/signup_success.html')