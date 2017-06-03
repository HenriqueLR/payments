#encoding: utf-8

from django.contrib import admin
from accounts.models import User, Profile, PasswordReset, Account


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(PasswordReset)
admin.site.register(Account)