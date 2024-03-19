from django.urls import path

from accounts import views


app_name = "accounts"


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signout/", views.signout, name="signout"),
    path('profile/', views.profile.update_profile, name='profile'),
    path('signup_success/', views.signup_success, name='signup_success'),
]
