from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
# Create your views here.
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages

class RegistrationViews(View):

	def get(self, request):
		return render(request, 'authentication/register.html')
	def post(self, request):
		# GET USER DATA

		# VALIDATE

		# Create aa user account

		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']

		context = {
			'fieldValues': request.POST
		}

		if not User.objects.filter(username=username).exists():
			if not User.objects.filter(email=email).exists():
				if len(password) < 6:
					messages.error(request, 'Password Too Short')
					return render(request, 'authentication/register.html', context)
				user = User.objects.create_user(username=username, email=email)
				user.set_password(password)
				user.save()
				messages.success(request, 'Account Sucessfully Created')
				return render(request, 'authentication/register.html')

		return render(request, 'authentication/register.html')



class UsernameValidationView(View):

	def post(self, request):
		data = json.loads(request.body)
		username = data['username']

		if not str(username).isalnum():
			return JsonResponse(
				{'username_error': 'username should only contain alphanumeric character'}, status=400)
		if User.objects.filter(username=username).exists():
			return JsonResponse(
				{'username_error': 'username is already occoupied'}, status=409)

		return JsonResponse(
				{'username_valid': True})


class EmailValidationView(View):

	def post(self, request):
		data = json.loads(request.body)
		email = data['email']

		if not validate_email(email):
			return JsonResponse(
				{'email_error': 'email is invalid'}, status=400)
		if User.objects.filter(email=email).exists():
			return JsonResponse(
				{'email_error': 'email is already occoupied'}, status=409)

		return JsonResponse(
				{'email_valid': True})
	

