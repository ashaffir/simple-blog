from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.SignupAPIView.as_view(), name="signup"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("profile/", views.UserProfile.as_view(), name="profile"),
]
