from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
	path('', views.index, name='incomes'),
	path('add-incomes', views.add_income, name="add-incomes"),
	path('edit-incomes/<int:id>', views.edit_income, name="edit-incomes"),
	path('delete-incomes/<int:id>', views.delete_income, name="delete-incomes"),
	path('search-incomes', csrf_exempt(views.search_incomes), name="search-incomes"),
	path('incomes/income-source-summary', views.income_source_sumary, name="income-source-summary"),
	path('income-summary', views.stastView, name='income-summary'),

]
