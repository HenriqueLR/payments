#encoding: utf-8

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()


def ajax_required(view):
	def wrap(request, *args, **kwargs):
		if not request.is_ajax():
			messages.error(request, 'Impossivel acessar o link, entre em contato com administrador do sistema.')
			return redirect('accounts:edit_profile')
		return view(request, *args, **kwargs)
	wrap.__doc__ = view.__doc__
	wrap.__name__ = view.__name__
	return wrap