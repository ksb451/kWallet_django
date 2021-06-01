from django.urls import path

from .views import RegistrationViews

urlpatterns = [
	path('register', RegistrationViews.as_view(), name="register")
	
]