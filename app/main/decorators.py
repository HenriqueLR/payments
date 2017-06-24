#encoding: utf-8

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from wallet.models import Debit, Deposit, Note
from main.utils import get_list_permissions


User = get_user_model()


def ajax_required(view):
	def wrap(request, *args, **kwargs):
		if not request.is_ajax():
			messages.error(request, 'Impossivel acessar o link, entre em contato com administrador do sistema.')
			return redirect('accounts:logout')
		return view(request, *args, **kwargs)
	wrap.__doc__ = view.__doc__
	wrap.__name__ = view.__name__
	return wrap

def permissions_denied(view):
	def wrap(request, *args, **kwargs):
		list_model = [Debit, Deposit, Note]
		for model in list_model:
			permissions = get_list_permissions(model, permission_list=['all'])
			if not request.user.has_perms(permissions):
				messages.error(request, 'Nao possui as permissoes necessarias, contate o administrador')
				return redirect('accounts:logout')
		return view(request, *args, **kwargs)
	wrap.__doc__ = view.__doc__
	wrap.__name__ = view.__name__
	return wrap


def verify_payment(view):
	def wrap(request, *args, **kwargs):
		if not request.user.account.status_payment:
			messages.error(request, 'Estamos aguardando o pagamento para liberacao do sistema')
			return redirect('accounts:logout')
		return view(request, *args, **kwargs)
	wrap.__doc__ = view.__doc__
	wrap.__name__ = view.__name__
	return wrap