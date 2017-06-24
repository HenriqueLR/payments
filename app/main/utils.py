#encoding: utf-8

import hashlib
import string
import random
import time
import calendar
from django.utils.safestring import mark_safe
from django.contrib.admin import ModelAdmin
from django.utils.text import capfirst
from django.apps import apps
from datetime import datetime
from django.conf import settings



IGNORE_MODELS = ("sites", "sessions", "admin",
    			 "contenttypes","auth")

ACCEPT_APPS = ("Profile", "User", "Debit", "Deposit", "Note")

MAP_URL = {
	"profile":"list_account",
	"user":"list_user",
	"home":"main",
	"debit":"list_debit",
	"deposit":"list_deposit",
	"note":"list_note",
}
ICON_MODEL = {
	"profile":"fa fa-address-book",
	"user":"fa fa-user",
	"home":"fa fa-home",
	"debit":"fa fa-pie-chart",
	"deposit":"fa fa-line-chart",
	"note":"fa fa-tags",
}
ICON_APPS = {
	"main":"fa fa-bars",
	"accounts":"fa fa-book",
	"wallet":"fa fa-id-card",
}


def apps_permissions(request):
	user = request.user
	app_dict = {}
	admin_class = ModelAdmin
	for model in apps.get_models():
		model_admin = admin_class(model, None)
		app_label = model._meta.app_label
		name = model._meta.verbose_name_plural

		if app_label in IGNORE_MODELS or name not in ACCEPT_APPS:
			continue
		has_module_perms = user.has_module_perms(app_label)
		if has_module_perms:
			#perms add change delete
			perms = model_admin.get_model_perms(request)
            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
			if True in perms.values():
				model_dict = {
                    'name': capfirst(name),
                    'admin_url': mark_safe('%s/%s/' % (app_label, model.__name__.lower())),
                    'app_url': ('%s/%s/') % (app_label, MAP_URL[model.__name__.lower()]),
                    'icon': ICON_MODEL[name.lower()],
                }

				if app_label in app_dict:
					app_dict[app_label]['models'].append(model_dict)
				else:
					app_dict[app_label] = {
                        'name': app_label.title(),
                        'app_url': app_label + '/',
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                        'icon':ICON_APPS[app_label.lower()],
                    }

	#include manual model
	url_manual_model = MAP_URL['home']
	include_dict = {}
	manual_model = {
		'name': 'Home',
		'admin_url': ('%s/') % (url_manual_model),
		'app_url': ('%s/') % (url_manual_model),
		'icon': ICON_MODEL['home'],
	}
	include_dict['main'] = {
	    'name': 'Main',
	    'app_url': ('%s/') % (url_manual_model),
	    'has_module_perms': True,
	    'icon':ICON_APPS['main'],
	    'models': [manual_model],
    }

	app_list = app_dict.values()
	#app_list.sort(key=lambda x: x['name'])

	#for app in app_list:
	#	app['models'].sort(key=lambda x: x['name'])

	app_list.insert(0, include_dict['main'])

	return app_list


def get_list_permissions(*args, **kwargs):
	list_permissions=[]
	if 'permission_list' in kwargs:
		permission_list = kwargs.pop('permission_list')

	for arg in args:
		[list_permissions.append(''.join([arg._meta.app_label,'.',x[0]]))
         for x in arg._meta.permissions for y in permission_list if y in x[0] or y == 'all']

	return list_permissions


def random_key(size=5):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))


def generate_hash_key(salt, random_str_size=5):
    random_str = random_key(random_str_size)
    text = random_str + salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


def format_date(date_start, date_end):
	date_start = datetime.strptime(''.join([date_start.strip(), ' 00:00:00']),
									settings.DATETIME_FORMAT_BR)
	date_end = datetime.strptime(''.join([date_end.strip(), ' 23:59:59']),
									settings.DATETIME_FORMAT_BR)

	return date_start, date_end


def get_period_this_month():
	date = datetime.now().date()
	_, num_days = calendar.monthrange(date.year, date.month)
	start_date = datetime.strptime(('%s/%s/%s 00:00:00') % ('01', date.month, date.year),
									settings.DATETIME_FORMAT_BR)
	end_date = datetime.strptime(('%s/%s/%s 23:59:59') % (num_days, date.month, date.year),
									settings.DATETIME_FORMAT_BR)
	return start_date, end_date


def format_json_graphic(list_objects, name):
	context = {'name':name, 'data': [],}
	for obj in list_objects:
		context['data'].append([time.mktime(obj['date'].timetuple()),
								int(str(obj['total']).split('.')[0])])
	return context