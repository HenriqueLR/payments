#encoding: utf-8

from django.utils.safestring import mark_safe
from django.contrib.admin import ModelAdmin
from django.utils.text import capfirst
from django.apps import apps



IGNORE_MODELS = ("sites", "sessions", "admin",
    			 "contenttypes","auth")

IGNORE_APPS = ("Profile")

MAP_URL = {
	"profile": "list_account",
}

def apps_permissions(request):
	user = request.user
	app_dict = {}
	admin_class = ModelAdmin
	for model in apps.get_models():
		model_admin = admin_class(model, None)
		app_label = model._meta.app_label
		name = model._meta.verbose_name_plural

		if app_label in IGNORE_MODELS or name not in IGNORE_APPS:
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
                }

				if app_label in app_dict:
					app_dict[app_label]['models'].append(model_dict)
				else:
					app_dict[app_label] = {
                        'name': app_label.title(),
                        'app_url': app_label + '/',
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }
	app_list = app_dict.values()

	app_list.sort(key=lambda x: x['name'])

	for app in app_list:
		app['models'].sort(key=lambda x: x['name'])

	return app_list


def get_list_permissions(*args, **kwargs):
	list_permissions=[]
	if 'permission_list' in kwargs:
		permission_list = kwargs.pop('permission_list')

	for arg in args:
		[list_permissions.append(''.join([arg._meta.app_label,'.',x[0]]))
         for x in arg._meta.permissions for y in permission_list if y in x[0] or y == 'all']

	return list_permissions
