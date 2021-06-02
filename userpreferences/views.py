from django.shortcuts import render
import os
import json
from django.conf import settings
import pdb
from .models import UserPreference
from django.contrib import messages
# Create your views here.


def index(request):
	exist = UserPreference.objects.filter(user=request.user).exists()
	if exist:
		user_preference = UserPreference.objects.get(user=request.user)
	else:
		user_preference = {}
	currency_data = []
	file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
	with open(file_path, 'r') as json_file:
		data = json.load(json_file)
		for k, v in data.items():
			currency_data.append({'name': k, 'value': v})
	if request.method == 'GET':
		# pdb.set_trace()
		return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preference': user_preference})
	else:
		currency = request.POST['currency']
		print(currency)
		if exist:
			user_preference.currency = currency
			user_preference.save()
			messages.success(request, 'Changes Saved')
		else:
			UserPreference.objects.create(user=request.user, currency=currency)
			messages.success(request, 'Changes Saved')
		return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preference': user_preference})
