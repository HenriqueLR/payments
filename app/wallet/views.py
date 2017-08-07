#encoding: utf-8

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from wallet.models import Debit, Deposit, Note
from wallet.forms import DebitForm, DepositForm, AddNoteForm, EditNoteForm
from wallet.permissions import (PermissionsDebitMixin, PermissionsDepositMixin,
                                PermissionsNoteMixin)
from main.utils import get_list_permissions, apps_permissions
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from main.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.utils.translation import to_locale, get_language



class DebitListView(PermissionsDebitMixin, ListView):

    model = Debit
    paginate_by = 10
    template_name = 'wallet/debit/list_debit.html'
    template_name_ajax = 'wallet/debit/list_debit_single.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class DebitDeleteView(PermissionsDebitMixin, DeleteView):

    model = Debit
    template_name = 'wallet/debit/debit_confirm_delete.html'
    template_name_ajax = 'wallet/debit/delete_debit_single.html'
    success_url = reverse_lazy('wallet:list_debit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(self.request, 'Lançamento de débito apagado com sucesso')
        except Exception as Error:
            messages.error(self.request, 'Ocorreu um erro ao apagar o lançamento, tente novamente')
        return HttpResponseRedirect(self.success_url)



class DebitDetailView(PermissionsDebitMixin, DetailView):

    model = Debit
    template_name = 'wallet/debit/detail_debit.html'
    template_name_ajax = 'wallet/debit/detail_debit_single.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class DebitUpdateView(PermissionsDebitMixin, UpdateView):

    model = Debit
    form_class = DebitForm
    template_name = 'wallet/debit/update_debit.html'
    template_name_ajax = 'wallet/debit/update_debit_modal.html'
    success_url = reverse_lazy('wallet:list_debit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Alterado com sucesso')
        except Exception as Error:
            messages.error(self.request, 'Erro ao alterar a débito, tente novamente')
        return HttpResponseRedirect(reverse_lazy('wallet:update_debit', kwargs={'pk': self.object.pk}))



class DebitAddView(PermissionsDebitMixin, CreateView):

    model = Debit
    form_class = DebitForm
    template_name = 'wallet/debit/add_debit.html'
    template_name_ajax = 'wallet/debit/add_debit_modal.html'
    success_url = reverse_lazy('wallet:add_debit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form):
        try:
            form.save(user=self.request.user)
            messages.success(self.request, 'Débito lançado com sucesso')
        except Exception as Error:
            messages.error(self.request, 'Erro ao lançar débito, tente novamente')
        return HttpResponseRedirect(self.success_url)


delete_debit = DebitDeleteView.as_view()
detail_debit = DebitDetailView.as_view()
update_debit = DebitUpdateView.as_view()
list_debit = DebitListView.as_view()
add_debit = DebitAddView.as_view()



class DepositListView(PermissionsDepositMixin, ListView):

    model = Deposit
    paginate_by = 10
    template_name = 'wallet/deposit/list_deposit.html'
    template_name_ajax = 'wallet/deposit/list_deposit_single.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class DepositDeleteView(PermissionsDepositMixin, DeleteView):

    model = Deposit
    template_name = 'wallet/deposit/deposit_confirm_delete.html'
    template_name_ajax = 'wallet/deposit/delete_deposit_single.html'
    success_url = reverse_lazy('wallet:list_deposit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        messages.success(self.request, 'Lançamento de déposito apagado com sucesso')
        return HttpResponseRedirect(self.success_url)



class DepositDetailView(PermissionsDepositMixin, DetailView):

    model = Deposit
    template_name = 'wallet/deposit/detail_deposit.html'
    template_name_ajax = 'wallet/deposit/detail_deposit_single.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class DepositUpdateView(PermissionsDepositMixin, UpdateView):

    model = Deposit
    form_class = DepositForm
    template_name = 'wallet/deposit/update_deposit.html'
    template_name_ajax = 'wallet/deposit/update_deposit_modal.html'
    success_url = reverse_lazy('wallet:list_deposit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Alterado com sucesso')
        return HttpResponseRedirect(reverse_lazy('wallet:update_deposit', kwargs={'pk': self.object.pk}))



class DepositAddView(PermissionsDepositMixin, CreateView):

    model = Deposit
    form_class = DepositForm
    template_name = 'wallet/deposit/add_deposit.html'
    template_name_ajax = 'wallet/deposit/add_deposit_modal.html'
    success_url = reverse_lazy('wallet:add_deposit')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form, **kwargs):
        form.save(user=self.request.user)
        messages.success(self.request, 'Déposito lançado com sucesso')
        return HttpResponseRedirect(self.success_url)


delete_deposit = DepositDeleteView.as_view()
detail_deposit = DepositDetailView.as_view()
update_deposit = DepositUpdateView.as_view()
list_deposit = DepositListView.as_view()
add_deposit = DepositAddView.as_view()



class NoteListView(PermissionsNoteMixin, ListView):

    model = Note
    paginate_by = 10
    template_name = 'wallet/note/list_note.html'
    template_name_ajax = 'wallet/note/list_note_single.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class NoteDeleteView(PermissionsNoteMixin, DeleteView):

    model = Note
    template_name = 'wallet/note/note_confirm_delete.html'
    template_name_ajax = 'wallet/note/delete_note_single.html'
    success_url = reverse_lazy('wallet:list_note')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        messages.success(self.request, 'Nota apagada com sucesso')
        return HttpResponseRedirect(self.success_url)



class NoteDetailView(PermissionsNoteMixin, DetailView):

    model = Note
    template_name = 'wallet/note/detail_note.html'
    required_permissions = get_list_permissions(model, permission_list=['all'])



class NoteUpdateView(PermissionsNoteMixin, UpdateView):

    model = Note
    form_class = EditNoteForm
    template_name = 'wallet/note/update_note.html'
    template_name_ajax = 'wallet/note/update_note_modal.html'
    success_url = reverse_lazy('wallet:list_note')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form, **kwargs):
        form.save()
        messages.success(self.request, 'Alterado com sucesso')
        return HttpResponseRedirect(reverse_lazy('wallet:update_note', kwargs={'pk': self.object.pk}))



class NoteAddView(PermissionsNoteMixin, CreateView):

    model = Note
    form_class = AddNoteForm
    template_name = 'wallet/note/add_note.html'
    template_name_ajax = 'wallet/note/add_note_modal.html'
    success_url = reverse_lazy('wallet:add_note')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def form_valid(self, form, **kwargs):
        form.save(user=self.request.user)
        messages.success(self.request, 'Nota criada com sucesso')
        return HttpResponseRedirect(self.success_url)


@login_required
@ajax_required
def update_status_note(request, pk):
    note = get_object_or_404(Note, pk=pk, account=request.user.account)
    note.status_note = not note.status_note
    note.save()
    return HttpResponse("ok")


def teste(request):
    return HttpResponse("ok")


delete_note = NoteDeleteView.as_view()
detail_note = NoteDetailView.as_view()
update_note = NoteUpdateView.as_view()
list_note = NoteListView.as_view()
add_note = NoteAddView.as_view()