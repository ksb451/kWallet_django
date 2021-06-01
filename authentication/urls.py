from django.urls import path

from .views import RegistrationViews, UsernameValidationView, EmailValidationView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
	path('register', RegistrationViews.as_view(), name="register"),
	path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
	path('validate-email', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
]