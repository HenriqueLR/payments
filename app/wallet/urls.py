#encoding: utf-8

from django.urls import path
from wallet.views import (delete_debit, detail_debit, update_debit,
						list_debit, add_debit, delete_deposit, detail_deposit,
						update_deposit, list_deposit, add_deposit, delete_note,
						detail_note, update_note, list_note, add_note, update_status_note,
						teste)

urlpatterns = [
	#debit urls
	path('delete_debit/<pk>', delete_debit, name='delete_debit'),
	path('detail_debit/<pk>', detail_debit, name='detail_debit'),
	path('update_debit/<pk>', update_debit, name='update_debit'),
	path('list_debit/', list_debit, name='list_debit'),
	path('add_debit/', add_debit, name='add_debit'),

	#deposit urls
	path('delete_deposit/<pk>', delete_deposit, name='delete_deposit'),
	path('detail_deposit/<pk>', detail_deposit, name='detail_deposit'),
	path('update_deposit/<pk>', update_deposit, name='update_deposit'),
	path('list_deposit/', list_deposit, name='list_deposit'),
	path('add_deposit/', add_deposit, name='add_deposit'),

	#note urls
	path('delete_note/<pk>', delete_note, name='delete_note'),
	path('detail_note/<pk>', detail_note, name='detail_note'),
	path('update_note/<pk>', update_note, name='update_note'),
	path('list_note/', list_note, name='list_note'),
	path('add_note/', add_note, name='add_note'),
	path('update_status_note/<pk>', update_status_note, name='update_status_note'),

	path('teste/', teste, name='teste'),
]