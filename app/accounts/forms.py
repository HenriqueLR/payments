#encoding: utf-8

from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Profile, Account
from django.contrib.auth.hashers import make_password
from accounts.localflavor.br import forms as brforms


User = get_user_model()


class AccountForm(forms.ModelForm):

    cpf = brforms.BRCPFField(error_messages={'required':'Campo obrigatorio.'},
                             required=True, label='Cpf', widget=forms.TextInput)

    class Meta:
        model = Account
        exclude = ['cpf', 'status_account']

    def save(self, commit=True):
        account = super(AccountForm, self).save(commit=False)
        account.cpf = self.cleaned_data['cpf']

        if commit:
            account.save()
        return account

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email':forms.TextInput(attrs = {'placeholder': 'Email'}),
        }

    def save(self, profile=None, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        user.username = profile.first_name.lower()

        if commit:
            user.save()
        return user


class AddUserForm(forms.ModelForm):

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email':forms.TextInput(attrs = {'placeholder': 'Email'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if (password1 and password2) and (password1 != password2):
            raise forms.ValidationError('senhas incorretas, verifique os campos.')
        return password2

    def save(self, profile=None, commit=True):
        user = super(AddUserForm, self).save(commit=False)
        user.password = make_password(password=self.cleaned_data['password1'], salt=None, hasher='default')
        user.username = profile.first_name.lower()

        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['id_profile', 'status_profile', 'order',
                   'created_at', 'updated_at', 'user']