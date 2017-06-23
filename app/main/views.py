#encoding: utf-8

import json
from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from main.utils import apps_permissions, format_json_graphic, get_period_this_month
from main.decorators import permissions_denied, ajax_required
from wallet.models import Debit, Deposit, Note
from django.http import HttpResponse, JsonResponse



@login_required
@permissions_denied
def home(request):
	template_name = 'main/home.html'
	total_deposit = Deposit.objects.sum_deposits(request.user)
	total_debit = Debit.objects.sum_debits(request.user)
	balance = (total_deposit - total_debit)
	debits = Debit.objects.list_debits(request.user)[:10]
	deposits = Deposit.objects.list_deposits(request.user)[:10]
	notes = Note.objects.list_notes(request.user)[:10]
	apps = apps_permissions(request)

	context = {'apps':apps, 'label_app':'Main', 'object_name':'Home',
			   'total_deposit':total_deposit, 'total_debit':total_debit,
			   'debits':debits, 'deposits':deposits, 'notes':notes,
			   'balance':balance}
	return render(request, template_name, context)


@login_required
@ajax_required
def graphics(request):
	if request.method == 'GET':
		list_graphics = []
		select_date = {"date": "to_date(cast(date_created as TEXT),'YYYY-MM-DD')", "created_at":"date_created"}
		list_graphics.append(format_json_graphic(Deposit.objects.filter(account=request.user.account).extra(select=select_date).values('date').annotate(total=Sum('value')).order_by('date')[:30],
							 Deposit._meta.verbose_name_plural))
		list_graphics.append(format_json_graphic(Debit.objects.filter(account=request.user.account).extra(select=select_date).values('date').annotate(total=Sum('value')).order_by('date')[:30],
							 Debit._meta.verbose_name_plural))

		return JsonResponse(list_graphics, safe=False)


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


def payment(request):
	return render(request, 'main/payment.html', {})