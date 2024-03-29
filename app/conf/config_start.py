#encoding: utf-8

import os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', sys.argv[1])
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from accounts.models import Account, Profile, User
from wallet.models import Debit, Deposit, Note
from conf import settings
from configparser import RawConfigParser

config = RawConfigParser()
config.read(''.join([str(settings.BASE_DIR), os.getenv('sys_arg', '')]))


User = get_user_model()


class ConfigStart(object):

	def __init__(self):
		self.email = config.get('user_config', 'EMAIL')
		self.password = config.get('user_config', 'PASSWORD')
		self.cpf = config.get('user_config', 'CPF')
		self.group_admin = 'customers'
		self.group_user = 'users'

	def create_account(self):
		account = Account(cpf=self.cpf, status_account=True, status_payment=True)
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
		group_admin = Group(name=self.group_admin)
		group_admin.save()
		self.set_permission_group(group_admin, User)
		self.set_permission_group(group_admin, Debit)
		self.set_permission_group(group_admin, Deposit)
		self.set_permission_group(group_admin, Note)

		group_user = Group(name=self.group_user)
		group_user.save()
		self.set_permission_group(group_user, Debit)
		self.set_permission_group(group_user, Deposit)
		self.set_permission_group(group_user, Note)

	def set_permission_group(self, group, model):
		permissions = Permission.objects.filter(codename__contains=model.__name__.lower())
		for permission in permissions:
			group.permissions.add(permission)
		group.save()



if __name__ == '__main__':
	try:
		config = ConfigStart()
		config.create_user(config.create_account())
		config.create_group()
	except Exception as Error:
		print(Error)
		pass