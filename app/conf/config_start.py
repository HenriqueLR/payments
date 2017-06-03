#encoding: utf-8

import os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings_production')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from accounts.models import Account
from conf import settings


User = get_user_model()


class ConfigStart(object):

	def __init__(self):
		self.email = settings.config.get('user_config', 'EMAIL')
		self.password = settings.config.get('user_config', 'PASSWORD')
		self.cpf = settings.config.get('user_config', 'CPF')
		self.group = 'customers'

	def create_account(self):
		account = Account(cpf=self.cpf, status_account=True)
		account.save()
		return account

	def create_user(self, account):
		user = User(email=self.email, password=self.password)
		user.account = account
		user.is_staff = True
		user.is_superuser = True
		user.is_active = True
		user.save()

	def create_group(self):
		group = Group(name=self.group)
		group.save()


if __name__ == '__main__':
	try:
		config = ConfigStart()
		config.create_user(config.create_account())
		config.create_group()
	except Exception as Error:
		print Error
		pass