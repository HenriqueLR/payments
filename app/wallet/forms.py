#encoding: utf-8

from django import forms
from wallet.models import Deposit, Debit, Note



class DebitForm(forms.ModelForm):

	def save(self, user=None, commit=True):
		debit = super(DebitForm, self).save(commit=False)
		if user:
			debit.author = user.username
			debit.account = user.account

		if commit:
			debit.save()
		return debit

	class Meta:
		model = Debit
		fields = ['origin', 'value', 'document', 'description', 'date_releases']
		widgets = {'value': forms.NumberInput(attrs={'min': 0})}



class DepositForm(forms.ModelForm):

	def save(self, user=None, commit=True):
		deposit = super(DepositForm, self).save(commit=False)
		if user:
			deposit.author = user.username
			deposit.account = user.account

		if commit:
			deposit.save()
		return deposit

	class Meta:
		model = Deposit
		fields = ['origin', 'value', 'document', 'description', 'date_releases']
		widgets = {'value': forms.NumberInput(attrs={'min': 0})}



class NoteForm(forms.ModelForm):

	def save(self, user=None, commit=True):
		note = super(NoteForm, self).save(commit=False)
		if user:
			note.author = user.username
			note.account = user.account

		if commit:
			note.save()
		return note

	class Meta:
		model = Note
		fields = ['title', 'status_alert', 'status_note', 'description', 'date_note']