#encoding: utf-8

from django import forms
from wallet.models import Debit



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
		fields = ['origin', 'value', 'document', 'description']
		widgets = {'value': forms.NumberInput(attrs={'min': 0})}

