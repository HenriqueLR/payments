#encoding: utf-8

import ast
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import Http404
from main.utils import apps_permissions
from datetime import datetime
from django.conf import settings



class PermissionsDebitMixin(object):

    @classmethod
    def as_view(cls):
        return login_required(super(PermissionsDebitMixin, cls).as_view())

    def get_queryset(self):
        qs = self.model.objects.list_debits(self.request.user)

        date = self.request.GET.get('date', '')
        if date != '':
            date = datetime.strptime(date, settings.DATE_FORMAT_BR)
            qs = qs.filter(created_at = date)
        return qs

    def get_context_data(self, **kwargs):
        context = super(PermissionsDebitMixin, self).get_context_data(**kwargs)
        context.update({'object_name':'Debit', 'apps':apps_permissions(self.request),
                        'label_app':'Wallet'})
        return context

    @method_decorator(never_cache)
    @method_decorator(user_passes_test(lambda u: u.is_active,login_url='accounts:logout'))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perms(self.required_permissions):
            raise Http404
        return super(PermissionsDebitMixin, self).dispatch(request, *args, **kwargs)