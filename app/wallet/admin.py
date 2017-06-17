#encoding: utf-8

from django.contrib import admin
from wallet.models import Debit, Deposit, Note


admin.site.register(Debit)
admin.site.register(Deposit)
admin.site.register(Note)