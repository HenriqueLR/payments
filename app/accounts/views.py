#encoding: utf-8

from django.views.generic.list import ListView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from accounts.models import Profile
from accounts.permissions import PermissionsAccountMixin
from accounts.forms import EditUserForm, ProfileForm, AddUserForm, AccountForm
from accounts.utils import AccountUtils
from main.utils import apps_permissions
from main.decorators import ajax_required


class AccountView(View):

    template_name = 'accounts/register/create_account.html'
    success_url = reverse_lazy('accounts:login')

    def get(self, request):
        context = {'form_profile': ProfileForm, 'form_user': AddUserForm,
                   'form_account': AccountForm}
        return render(self.request, self.template_name, context)

    def post(self, request):
        form_profile = ProfileForm(self.request.POST or None)
        form_user = AddUserForm(self.request.POST or None)
        form_account = AccountForm(self.request.POST or None)

        if form_profile.is_valid() and form_user.is_valid() and form_account.is_valid():
            try:
                profile = form_profile.save(commit=False)
                user = form_user.save(profile=profile, commit=False)
                user.account = form_account.save()
                user.save()
                profile.user = user
                profile.save()
                messages.success(self.request, 'Conta criada com sucesso !')
                return HttpResponseRedirect(self.success_url)
            except Exception as Error:
                messages.error(self.request, Error)
        context = {'form_profile': form_profile, 'form_user': form_user,
                   'form_account': form_account}
        return render(self.request, self.template_name, context)



class AccountListView(PermissionsAccountMixin, ListView):

    paginate_by = 5
    model = Profile
    template_name = 'accounts/register/list_account.html'
    success_url = reverse_lazy('accounts:login')


list_account = AccountListView.as_view()
create_account = AccountView.as_view()


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='accounts:logout')
def active_account(request, pk):
    account = AccountUtils(get_object_or_404(Profile, pk=pk))
    try:
        account.active_account(True)
        account.add_user_group()
        account.save_account()
        messages.success(request, 'Conta ativada.')
    except Exception as Error:
        account.roll_back()
        messages.error(request, Error)
    return HttpResponseRedirect(reverse_lazy('accounts:list_account'))


@login_required
@user_passes_test(lambda u: u.is_active, login_url='accounts:logout')
@ajax_required
def edit_password(request):
    template_name = 'accounts/user/reset_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso.')
            update_session_auth_hash(request, form.user)
            return HttpResponse('ok')
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_active, login_url='accounts:logout')
def edit_profile(request):
    template_name = 'accounts/user/edit_profile.html'
    form_user = EditUserForm(request.POST or None, instance=request.user)
    form_profile = AddProfileForm(request.POST or None,
                                  instance=get_object_or_404(Profile, user=request.user))
    if form_user.is_valid() and form_profile.is_valid():
        form_user.save(profile=form_profile.save())
        messages.success( request, 'Os dados da sua conta foram alterados com sucesso!')
        return redirect('accounts:edit_profile')
    context = {'form_profile':form_profile, 'form_user':form_user,
               'object_name':'Profile', 'apps':apps_permissions(request),'label_app':'None',}
    return render(request, template_name, context)