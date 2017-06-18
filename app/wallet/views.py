#encoding: utf-8

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from wallet.models import Debit, Deposit, Note
from wallet.forms import DebitForm, DepositForm, NoteForm
from wallet.permissions import (PermissionsDebitMixin, PermissionsDepositMixin,
                                PermissionsNoteMixin)
from main.utils import get_list_permissions, apps_permissions
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from main.decorators import ajax_required



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



class NoteListView(PermissionsNoteMixin, ListView):

    model = Note
    paginate_by = 10
    template_name = 'wallet/note/list_note.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            note = get_object_or_404(Note, pk=self.request.GET.get('note'), account=self.request.user.account)
            note.status_note = not note.status_note
            note.save()
        return super(NoteListView, self).get(self.request, *args, **kwargs)



class NoteDeleteView(PermissionsNoteMixin, DeleteView):

    model = Note
    template_name = 'wallet/note/note_confirm_delete.html'
    success_url = reverse_lazy('wallet:list_note')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(self.request, 'Nota apagada com sucesso')
        except Exception as Error:
            messages.error(self.request, 'Ocorreu um erro para apagar a nota, tente novamente')
        return HttpResponseRedirect(self.success_url)



class NoteDetailView(PermissionsNoteMixin, DetailView):

    model = Note
    template_name = 'wallet/note/detail_note.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class NoteUpdateView(PermissionsNoteMixin, UpdateView):

    model = Note
    form_class = NoteForm
    template_name = 'wallet/note/update_note.html'
    success_url = reverse_lazy('wallet:list_note')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form):
        messages.success(self.request, 'Alterado com sucesso')
        return super(NoteUpdateView, self).form_valid(form)



class NoteAddView(PermissionsNoteMixin, CreateView):

    model = Note
    form_class = NoteForm
    template_name = 'wallet/note/add_note.html'
    success_url = reverse_lazy('wallet:add_note')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form):
        try:
            form.save(user=self.request.user)
            messages.success(self.request, 'Nota criada com sucesso')
        except Exception as Error:
            messages.error(self.request, 'Erro ao criar nota, tente novamente')
        return super(NoteAddView, self).form_valid(form)


delete_note = NoteDeleteView.as_view()
detail_note = NoteDetailView.as_view()
update_note = NoteUpdateView.as_view()
list_note = NoteListView.as_view()
add_note = NoteAddView.as_view()