#encoding: utf-8

from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from accounts.models import Profile, PasswordReset, User
from accounts.permissions import PermissionsAccountMixin, PermissionsUserMixin
from accounts.forms import EditUserForm, ProfileForm, AddUserForm, AccountForm, PasswordResetForm
from accounts.utils import AccountUtils
from main.utils import apps_permissions, get_list_permissions
from main.decorators import ajax_required
from main.mail import send_mail_confirm_account



class AccountView(View):

    template_name = 'accounts/register/create_account.html'
    success_url = reverse_lazy('accounts:create_account')

    def get(self, request):
        context = {'form_profile': ProfileForm, 'form_user': AddUserForm,
                   'form_account': AccountForm, 'url_payment': reverse_lazy('main:payment')}
        return render(self.request, self.template_name, context)

    def post(self, request):
        form_profile = ProfileForm(self.request.POST or None)
        form_user = AddUserForm(self.request.POST or None)
        form_account = AccountForm(self.request.POST or None)

        if form_profile.is_valid() and form_user.is_valid() and form_account.is_valid():
            profile = form_profile.save(commit=False)
            user = form_user.save(profile=profile, commit=False)
            user.account = form_account.save()
            user.save()

            profile.user = user
            profile.order = Profile.ORDER_CHOICE[0][0]
            profile.save()

            account = AccountUtils(profile)
            account.active_account(True)
            account.add_user_group('customers')
            account.save_account()

            messages.info(self.request,'Cadastro criado com sucesso, aguarde para ser redirecionado '+\
                          'para tela de pagamento ou clique')

            try:
                send_mail_confirm_account(profile)
            except Exception as Error:
                pass

            return HttpResponseRedirect(self.success_url)

        context = {'form_profile': form_profile, 'form_user': form_user,
                   'form_account': form_account, 'url_payment': reverse_lazy('main:payment')}
        return render(self.request, self.template_name, context)


class AccountListView(PermissionsAccountMixin, ListView):

    model = Profile
    paginate_by = 5
    template_name = 'accounts/register/list_account.html'
    success_url = reverse_lazy('accounts:login')
    required_permissions = get_list_permissions(model, permission_list=['all'])


class UserListView(PermissionsUserMixin, ListView):

    model = User
    paginate_by = 5
    template_name = 'accounts/user/list_user.html'
    success_url = reverse_lazy('accounts:login')
    required_permissions = get_list_permissions(model, permission_list=['all'])


@login_required
@user_passes_test(lambda u: u.groups.filter(name='customers').exists(),
                                            login_url='accounts:logout')
def edit_user(request, pk):
    template_name = 'accounts/user/edit_user.html'
    user = get_object_or_404(User, pk=pk, account=request.user.account)
    form_user = EditUserForm(request.POST or None, instance=user)
    form_profile = ProfileForm(request.POST or None,
                                  instance=get_object_or_404(Profile, user=user))
    if form_user.is_valid() and form_profile.is_valid():
        form_user.save(profile=form_profile.save())
        messages.success(request, 'Os dados da sua conta foram alterados com sucesso')
    context = {'form_profile':form_profile, 'form_user':form_user, 'object_name':'User',
               'apps':apps_permissions(request),'label_app':'Accounts', 'object':user}
    return render(request, template_name, context)


class UserDeleteView(PermissionsUserMixin, DeleteView):

    model = User
    template_name = 'accounts/user/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:list_user')
    required_permissions = get_list_permissions(model, permission_list=['all'])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(self.request, 'Usuário removido')
        except Exception as Error:
            messages.error(self.request, 'Tente novamente, ocorreu um erro')
        return HttpResponseRedirect(self.success_url)


delete_user = UserDeleteView.as_view()
list_user = UserListView.as_view()
list_account = AccountListView.as_view()
create_account = AccountView.as_view()


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='accounts:logout')
def active_account(request, pk):
    account = AccountUtils(get_object_or_404(Profile, pk=pk))
    try:
        if account.check_status():
            messages.warning(request, 'Esta conta já está ativa.')
            return HttpResponseRedirect(reverse_lazy('accounts:list_account'))
        account.active_payment()
        messages.success(request, 'Conta ativada')
    except Exception as Error:
        account.roll_back()
        messages.error(request, Error)
    return HttpResponseRedirect(reverse_lazy('accounts:list_account'))


@login_required
@ajax_required
def edit_password(request):
    template_name = 'accounts/user/edit_password.html'
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso')
            update_session_auth_hash(request, form.user)
            return HttpResponse('ok')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {"form": form}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
@ajax_required
@user_passes_test(lambda u: u.groups.filter(name='customers').exists(),
                                            login_url='accounts:logout')
def edit_password_user(request, pk):
    template_name = 'accounts/user/edit_password_user.html'
    user = get_object_or_404(User, pk=pk, account=request.user.account)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso')
            update_session_auth_hash(request, form.user)
            return HttpResponse('ok')
    else:
        form = PasswordChangeForm(user=user)
    context = {"object":user, "form": form}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
def edit_profile(request):
    template_name = 'accounts/user/edit_profile.html'
    form_user = EditUserForm(request.POST or None, instance=request.user)
    form_profile = ProfileForm(request.POST or None,
                                  instance=get_object_or_404(Profile, user=request.user))
    if form_user.is_valid() and form_profile.is_valid():
        form_user.save(profile=form_profile.save())
        messages.success(request, 'Os dados do seu perfil foram alterados com sucesso')
        return redirect('accounts:edit_profile')
    context = {'form_profile':form_profile, 'form_user':form_user,
               'object_name':'Profile', 'apps':apps_permissions(request),'label_app':'None',}
    return render(request, template_name, context)


@login_required
def detail_profile(request):
    context = {'profile': get_object_or_404(Profile, user=request.user),
               'app_label':None, 'object_name':None, 'apps':apps_permissions(request)}
    template_name = 'accounts/user/detail_profile.html'
    return render(request, template_name, context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='customers').exists(),
                                            login_url='accounts:logout')
def create_user(request):
    template_name = 'accounts/user/create_user.html'
    form_user = AddUserForm(request.POST or None)
    form_profile = ProfileForm(request.POST or None)

    if form_user.is_valid() and form_profile.is_valid():
        try:
            profile = form_profile.save(commit=False)
            user = form_user.save(profile=profile, commit=False)
            user.account = request.user.account
            user.is_active = True
            user.save()
            profile.user = user
            profile.order = Profile.ORDER_CHOICE[1][0]
            profile.status_profile = True
            profile.save()
            accounts = AccountUtils(profile)
            accounts.add_user_group('users')
            messages.success(request, 'Usuário criado com sucesso')
            return redirect('accounts:list_user')
        except Exception as Error:
            messages.error(request, 'Ocorreu um erro, tente novamente')

    context = {'form_profile':form_profile, 'form_user':form_user,
               'object_name':'User', 'apps':apps_permissions(request),'label_app':'Accounts',}
    return render(request, template_name, context)


@ajax_required
def reset_password(request):
    template_name = 'accounts/auth/reset_password.html'
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Entre no seu e-mail, e confirme o link para resetar a sua senha')
        return HttpResponse('ok')
    context = {'form':form}
    return render(request, template_name, context)


def confirm_reset_password(request):
    template_name = 'accounts/register/confirm_reset_password.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=request.GET.get('key', ''), confirmed=False)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        reset.confirmed = True
        reset.save()
        messages.success(request, 'Senha alterada com sucesso')
        return HttpResponseRedirect(reverse_lazy('accounts:login'))
    context['form'] = form
    return render(request, template_name, context)