#encoding: utf-8

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render
from wallet.models import Debit, Deposit
from wallet.forms import DebitForm, DepositForm
from wallet.permissions import PermissionsDebitMixin, PermissionsDepositMixin
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



class DepositListView(PermissionsDepositMixin, ListView):

    model = Deposit
    paginate_by = 10
    template_name = 'wallet/deposit/list_deposit.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class DepositDeleteView(PermissionsDepositMixin, DeleteView):

    model = Deposit
    template_name = 'wallet/deposit/deposit_confirm_delete.html'
    success_url = reverse_lazy('wallet:list_deposit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(self.request, 'Lancamento de Deposito apagado com sucesso')
        except Exception as Error:
            messages.error(self.request, 'Ocorreu um erro ao apagar o lancamento, tente novamente')
        return HttpResponseRedirect(self.success_url)



class DepositDetailView(PermissionsDepositMixin, DetailView):

    model = Deposit
    template_name = 'wallet/deposit/detail_deposit.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class DepositUpdateView(PermissionsDepositMixin, UpdateView):

    model = Deposit
    form_class = DepositForm
    template_name = 'wallet/deposit/update_deposit.html'
    success_url = reverse_lazy('wallet:list_deposit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form):
        messages.success(self.request, 'Alterado com sucesso.')
        return super(DepositUpdateView, self).form_valid(form)



class DepositAddView(PermissionsDepositMixin, CreateView):

    model = Deposit
    form_class = DepositForm
    template_name = 'wallet/deposit/add_deposit.html'
    success_url = reverse_lazy('wallet:add_deposit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form):
        try:
            form.save(user=self.request.user)
            messages.success(self.request, 'Debito lancado com sucesso')
        except Exception as Error:
            messages.error(self.request, 'Erro ao lancar debito, tente novamente')
        return super(DepositAddView, self).form_valid(form)


delete_deposit = DepositDeleteView.as_view()
detail_deposit = DepositDetailView.as_view()
update_deposit = DepositUpdateView.as_view()
list_deposit = DepositListView.as_view()
add_deposit = DepositAddView.as_view()