# from django.views.generic import View
# from django.shortcuts import render, redirect
# from accounts.forms import MyCustomSignUpForm


# class SignUpView(View):
#     """User registration view with email verification"""

#     template_name = "accounts/signup.html"
#     form_class = MyCustomSignUpForm

#     def get(self, request, *args, **kwargs):
#         forms = self.form_class()
#         context = {"form": forms}
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         forms = self.form_class(request.POST)
#         if forms.is_valid():
#             forms.save()
#             return redirect("accounts:signin")
#         context = {"form": forms}
#         return render(request, self.template_name, context)
