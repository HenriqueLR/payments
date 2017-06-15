#encoding: utf-8

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render
from wallet.models import Debit
from wallet.forms import DebitForm
from wallet.permissions import PermissionsDebitMixin
from main.utils import get_list_permissions, apps_permissions
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages



class DebitListView(PermissionsDebitMixin, ListView):

    model = Debit
    paginate_by = 10
    template_name = 'wallet/debit/list_debit.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class DebitDeleteView(PermissionsDebitMixin, DeleteView):

    model = Debit
    template_name = 'wallet/debit/debit_confirm_delete.html'
    success_url = reverse_lazy('wallet:list_debit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(self.request, 'Lancamento de debito apagado com sucesso')
        except Exception as Error:
            messages.error(self.request, 'Ocorreu um erro ao apagar o lancamento, tente novamente')
        return HttpResponseRedirect(self.success_url)



class DebitDetailView(PermissionsDebitMixin, DetailView):

    model = Debit
    template_name = 'wallet/debit/detail_debit.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class DebitUpdateView(PermissionsDebitMixin, UpdateView):

    model = Debit
    form_class = DebitForm
    template_name = 'wallet/debit/update_debit.html'
    success_url = reverse_lazy('wallet:list_debit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form):
        messages.success(self.request, 'Alterado com sucesso.')
        return super(DebitUpdateView, self).form_valid(form)



class DebitAddView(PermissionsDebitMixin, CreateView):

    model = Debit
    form_class = DebitForm
    template_name = 'wallet/debit/add_debit.html'
    success_url = reverse_lazy('wallet:add_debit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form):
        try:
            form.save(user=self.request.user)
            messages.success(self.request, 'Debito lancado com sucesso')
        except Exception as Error:
            messages.error(self.request, 'Erro ao lancar debito, tente novamente')
        return super(DebitAddView, self).form_valid(form)


delete_debit = DebitDeleteView.as_view()
detail_debit = DebitDetailView.as_view()
update_debit = DebitUpdateView.as_view()
list_debit = DebitListView.as_view()
add_debit = DebitAddView.as_view()