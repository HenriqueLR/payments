#encoding: utf-8

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from main.utils import apps_permissions


#CRIAR DECORATOR PARA VERIFICAR AS PERMISSIONS DE CADA MODEL QUE FOR USAR.
@login_required
@user_passes_test(lambda u: u.is_active, login_url='accounts:logout')
def home(request):
	context = {'apps':apps_permissions(request),
			   'label_app': 'Main', 'object_name': 'Home'}
	return render(request, 'main/home.html', context)