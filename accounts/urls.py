from django.urls import path
from accounts.views import RegisterView, ProfileView, ProfileUpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile-edit"),
    path('password_reset/', PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html'), name='password_reset'),
]
