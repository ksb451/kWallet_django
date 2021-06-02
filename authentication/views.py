from django.shortcuts import render, redirect, reverse
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages, auth
from django.core.mail import EmailMessage

from django.utils.encoding import force_text, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from .utils import token_generator

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
				user.is_active = False
				user.save()

				# 
				# 
				# 
				# 
				uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
				domain = get_current_site(request).domain
				relative_link = reverse('activate', kwargs={
										'uidb64': uidb64, 'token': token_generator.make_token(user)})
				
				activate_url = 'http://'+domain+relative_link

				email_subject = "Activate your account"
				email_body = "Hii "+user.username+", Please use this linnk to verify your account\n" + activate_url

				email = EmailMessage(
					email_subject,
					email_body,
					'noreply@semycolon.com',
					[email],
					)
				email.send(fail_silently=False)
				messages.success(request, 'Account Sucessfully Created')
				return render(request, 'authentication/register.html')

		return render(request, 'authentication/register.html')


class verificationView(View):
	def get(self, request, uidb64, token):
		try:
			print('starting to activate')
			idd = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=idd)

			if not token_generator.check_token(user, token):
				print('already activated')
				return redirect('login'+'?message='+'User Already Activated')

			if user.is_active:
				print('already activated')
				return redirect('login')
			user.is_active = True
			user.save()
			print('activated')
			messages.success(request, 'Account Activatd Sucessfully')
			return redirect('login')

		except Exception as e:
			print(e)
			pass

		return redirect('login')


class LoginView(View):
	def get(self, request):
		return render(request, 'authentication/login.html')

	def post(self, 	request):
		username = request.POST['username']
		password = request.POST['password']
		
		if username and password:
			user = auth.authenticate(username=username, password=password)

			if user:
				if user.is_active:
					auth.login(request, user)
					messages.success(request, 'Welcome, '+user.username+" You Are Now logged in")
					return redirect('index')

				# system_messages = messages.get_messages(request)
				# for message in system_messages:
				# 	# This iteration is necessary
				# 	pass
				messages.error(request, 'Account is not Active Plesase acheck your email')
				return render(request, 'authentication/login.html')
			
			messages.error(request, 'Invalid credentials Try again')
			return render(request, 'authentication/login.html')
		
		messages.error(request, 'Please fill all Fields')
		return render(request, 'authentication/login.html')


class logoutView(View):
	def post(self, request):
		auth.logout(request)
		messages.success(request, 'You have been logged Out')
		return redirect('login')




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
	

