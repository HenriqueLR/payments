#encoding: utf-8

from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import Http404
from main.utils import apps_permissions, format_date



class PermissionsGeralMixin(object):

    @classmethod
    def as_view(cls):
        return login_required(super(PermissionsGeralMixin, cls).as_view())

    @method_decorator(never_cache)
    @method_decorator(user_passes_test(lambda u: u.is_active,login_url='accounts:logout'))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perms(self.required_permissions):
            raise Http404
        return super(PermissionsGeralMixin, self).dispatch(request, *args, **kwargs)



class PermissionsNoteMixin(PermissionsGeralMixin):

    def get_queryset(self):
        qs = self.model.objects.list_notes(self.request.user)

        date = self.request.GET.get('date', '')
        if date != '':
            range_date = date.split('-')
            date_start, date_end = format_date(range_date[0], range_date[1])
            qs = qs.filter(date_note__gte=date_start, date_note__lte=date_end)

        note = self.request.GET.get('status_note', '')
        if note != '' and note != 'all':
            qs = qs.filter(status_note=eval(note))

        alert = self.request.GET.get('status_alert', '')
        if alert != '' and alert != 'all':
            qs = qs.filter(status_alert=eval(alert))

        return qs

    def get_context_data(self, **kwargs):
        context = super(PermissionsNoteMixin, self).get_context_data(**kwargs)
        context.update({'object_name':'Note', 'apps':apps_permissions(self.request),
                        'label_app':'Wallet'})
        return context



class PermissionsDebitMixin(PermissionsGeralMixin):

    def get_queryset(self):
        qs = self.model.objects.list_debits(self.request.user)

        date = self.request.GET.get('date', '')
        if date != '':
            range_date = date.split('-')
            date_start, date_end = format_date(range_date[0], range_date[1])
            qs = qs.filter(created_at__gte=date_start, created_at__lte=date_end)

        return qs

    def get_context_data(self, **kwargs):
        context = super(PermissionsDebitMixin, self).get_context_data(**kwargs)
        context.update({'object_name':'Debit', 'apps':apps_permissions(self.request),
                        'label_app':'Wallet'})
        return context



class PermissionsDepositMixin(PermissionsGeralMixin):

    def get_queryset(self):
        qs = self.model.objects.list_deposits(self.request.user)

        date = self.request.GET.get('date', '')
        if date != '':
            range_date = date.split('-')
            date_start, date_end = format_date(range_date[0], range_date[1])
            qs = qs.filter(created_at__gte=date_start, created_at__lte=date_end)

        return qs

    def get_context_data(self, **kwargs):
        context = super(PermissionsDepositMixin, self).get_context_data(**kwargs)
        context.update({'object_name':'Deposit', 'apps':apps_permissions(self.request),
                        'label_app':'Wallet'})
        return context