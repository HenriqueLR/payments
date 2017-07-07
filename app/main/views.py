#encoding: utf-8

import json
from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from main.utils import apps_permissions, format_json_graphic, get_period_this_month
from main.decorators import permissions_denied, ajax_required, verify_payment
from wallet.models import Debit, Deposit, Note
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext as _



def payment(request):
	return render(request, 'main/payment.html', {})


@login_required
@verify_payment
def home(request):
	template_name = 'main/home.html'
	apps = apps_permissions(request)
	context = {'apps':apps,'label_app':'Main','object_name':'Home'}
	return render(request, template_name, context)


@login_required
@ajax_required
def graphics(request):
	if request.method == 'GET':
		list_graphics = []
		select_date = {"date": "to_date(cast(date_releases as TEXT),'YYYY-MM-DD')", "created_at":"date_releases"}
		list_graphics.append(format_json_graphic(Deposit.objects.filter(account=request.user.account)\
							.extra(select=select_date).values('date').annotate(total=Sum('value')).order_by('date')[:30],
							 _(Deposit._meta.verbose_name_plural)))
		list_graphics.append(format_json_graphic(Debit.objects.filter(account=request.user.account)\
							.extra(select=select_date).values('date').annotate(total=Sum('value')).order_by('date')[:30],
							 _(Debit._meta.verbose_name_plural)))
		return JsonResponse(list_graphics, safe=False)


@login_required
@ajax_required
def balance(request):
	template_name = 'main/balance.html'
	total_deposit = Deposit.objects.sum_deposits(request.user)
	total_debit = Debit.objects.sum_debits(request.user)
	balance = (total_deposit - total_debit)
	context = {'total_deposit':total_deposit,'total_debit':total_debit,'balance':balance}
	return render(request, template_name, context)


@login_required
@ajax_required
def alerts(request):
	template_name = 'main/alerts.html'
	if request.method == 'GET':
		start_date, end_date = get_period_this_month()
		alerts = Note.objects.filter(status_alert=True, account=request.user.account,
									 date_note__gte=start_date, date_note__lte=end_date,
									 status_note=True)
		return render(request, template_name, {'alerts':alerts})


@login_required
@ajax_required
def list_note(request):
	template_name = 'wallet/note/list_note_single.html'
	notes = Note.objects.list_notes(request.user)[:10]
	return render(request, template_name, {'objects':notes})


@login_required
@ajax_required
def delete_note(request, pk):
	Note.objects.filter(pk=pk, account=request.user.account).delete()
	return HttpResponse("ok")


@login_required
@ajax_required
def list_debit(request):
	template_name = 'wallet/debit/list_debit_single.html'
	debits = Debit.objects.list_debits(request.user)[:10]
	return render(request, template_name, {'objects':debits})


@login_required
@ajax_required
def delete_debit(request, pk):
	Debit.objects.filter(pk=pk, account=request.user.account).delete()
	return HttpResponse("ok")


@login_required
@ajax_required
def list_deposit(request):
	template_name = 'wallet/deposit/list_deposit_single.html'
	deposits = Deposit.objects.list_deposits(request.user)[:10]
	return render(request, template_name, {'objects':deposits})


@login_required
@ajax_required
def delete_deposit(request, pk):
	Deposit.objects.filter(pk=pk, account=request.user.account).delete()
	return HttpResponse("ok")