#encoding: utf-8

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()



class AccountUtils(object):

	def __init__(self, profile):
		self.profile = profile
		self.user = profile.user
		self.account = profile.user.account

	def active_account(self, status):
		self.profile.status_profile = status
		self.user.is_active = status
		self.account.status_account = status

	def create_user(self):
		user = User(password=self.account.password, email=self.account.email,
					first_name=self.account.first_name, last_name=self.account.last_name,
					state=self.account.state)
		user.save()
		return user

	def add_user_group(self, group):
		gp = Group.objects.get(name=group)
		gp.user_set.add(self.user)

	def check_status(self):
		if (self.profile.status_profile and self.user.is_active
			and self.account.status_account):
			return True

	def save_user(self):
		self.user.save()
		self.profile.save()

	def save_account(self):
		self.account.save()
		self.user.save()
		self.profile.save()

	def roll_back(self):
		self.active_account(False)
		self.save_account()