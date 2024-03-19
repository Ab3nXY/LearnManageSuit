from django.urls import path

from accounts import views


app_name = "accounts"


urlpatterns = [
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signout/", views.signout, name="signout"),
    path('profile/', views.profile.update_profile, name='profile'),
]
