#encoding: utf-8

from django.contrib import admin
from wallet.models import Debit, Deposit


admin.site.register(Debit)
admin.site.register(Deposit)