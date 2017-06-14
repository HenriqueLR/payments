#encoding: utf-8

import ast
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.http import Http404
from main.utils import apps_permissions



class PermissionsAccountMixin(object):

    @classmethod
    def as_view(cls):
        return login_required(super(PermissionsAccountMixin, cls).as_view())

    def get_queryset(self):
        qs = self.model.objects.list_account(self.request.user)

        order = self.request.GET.get('order', '')
        if order != '' and order != 'all':
            qs = qs.filter(order=order)

        return qs

    def get_context_data(self, **kwargs):
        context = super(PermissionsAccountMixin, self).get_context_data(**kwargs)
        context.update({'object_name':'Profile', 'apps':apps_permissions(self.request),
                        'label_app':'Accounts'})
        return context

    @method_decorator(never_cache)
    @method_decorator(user_passes_test(lambda u: u.is_superuser,login_url='accounts:logout'))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perms(self.required_permissions):
            raise Http404
        return super(PermissionsAccountMixin, self).dispatch(request, *args, **kwargs)



class PermissionsUserMixin(object):

    @classmethod
    def as_view(cls):
        return login_required(super(PermissionsUserMixin, cls).as_view())

    def get_queryset(self):
        qs = self.model.objects.list_user(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super(PermissionsUserMixin, self).get_context_data(**kwargs)
        context.update({'object_name':'User', 'apps':apps_permissions(self.request),
                        'label_app':'Accounts'})
        return context

    @method_decorator(never_cache)
    @method_decorator(user_passes_test(lambda u: u.is_active, login_url='accounts:logout'))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perms(self.required_permissions):
            raise Http404
        return super(PermissionsUserMixin, self).dispatch(request, *args, **kwargs)