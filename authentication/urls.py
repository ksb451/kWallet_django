from django.urls import path

from .views import RegistrationViews, UsernameValidationView, EmailValidationView, verificationView, LoginView, logoutView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
	path('register', RegistrationViews.as_view(), name="register"),
	path('login', LoginView.as_view(), name="login"),
	path('logout', logoutView.as_view(), name="logout"),
	path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
	path('validate-email', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
	path('activate/<uidb64>/<token>', verificationView.as_view(), name='activate'),
]