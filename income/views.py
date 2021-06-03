from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Source, UserIncome
from userpreferences.models import UserPreference
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
# Create your views here.


def search_incomes(request):
	if request.method == 'POST':
		search_str = json.loads(request.body).get('searchText')

		incomes = UserIncome.objects.filter(
			amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
			date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
			description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
			source__icontains=search_str, owner=request.user)
		data = incomes.values()
		return JsonResponse(list(data), safe=False)





@login_required(login_url='/authentication/login')
def index(request):
	sources = Source.objects.all()
	incomes = UserIncome.objects.filter(owner=request.user)
	
	exists = UserPreference.objects.filter(user=request.user).exists()
	preferences = {}
	if exists:
		preferences = UserPreference.objects.get(user=request.user)
	else:
		preferences = {'currency': 'None'}
	
	paginator = Paginator(incomes, 2)
	page_number = request.GET.get('page')
	page_obj = Paginator.get_page(paginator, page_number)

	context = {
		'userincomes': incomes,
		'preferences': preferences,
		'page_obj': page_obj,
	}

	return render(request, 'income/index.html', context)


def add_income(request):
	sources = Source.objects.all()
	
	if request.method == 'GET':
		context = {
			'sources': sources
		}
		return render(request, 'income/add_income.html', context)

	if request.method == 'POST':
		amount = request.POST['amount']
		description = request.POST['description']
		income_date = request.POST['income_date']
		context = {
			'sources': sources,
			'values': request.POST
		}
		if not amount:
			messages.error(request, 'Amount is required')
			return render(request, 'income/add_income.html', context)
		if not description:
			messages.error(request, 'Description is required')
			return render(request, 'income/add_income.html', context)
		if not income_date:
			messages.error(request, 'Date is required')
			return render(request, 'income/add_income.html', context)
		
		source = request.POST['source']

		UserIncome.objects.create(amount=amount, date=income_date, description=description, owner=request.user, source=source)
		messages.success(request, 'Income added successfully')
		return redirect('incomes')


def edit_income(request, id):
	income = UserIncome.objects.get(pk=id)
	sources = Source.objects.all()
	context = {
		'income': income,
		'sources': sources
	}
	if request.method == 'GET':
		return render(request, 'income/edit_income.html', context)
	if request.method == 'POST':
		amount = request.POST['amount']
		description = request.POST['description']
		context = {
			'sources': sources,
			'income': income,
			'values': request.POST
		}
		if not amount:
			messages.error(request, 'Amount is required')
			return render(request, 'income/edit_income.html', context)
		if not description:
			messages.error(request, 'Description is required')
			return render(request, 'income/edit_income.html', context)
		income_date = request.POST['income_date']
		source = request.POST['source']
		income.owner = request.user
		income.amount = amount
		income.date = income_date
		income.description = description
		income.source = source
		income.save()

		messages.success(request, 'Income edited successfully')
		return redirect('incomes')


def delete_income(request, id):
	income = UserIncome.objects.get(pk=id)
	income.delete()
	messages.success(request, 'Income deleted successfully')
	return redirect('incomes')