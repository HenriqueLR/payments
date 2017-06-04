#encoding: utf-8

import re
from django.db.models import Q
from django.db import models
from django.conf import settings
from django.core import validators
from accounts.localflavor.br.br_states import STATE_CHOICES
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)



class Account(models.Model):

    id_account = models.AutoField(primary_key=True, verbose_name=u'Cod Account', db_column='id_account')
    cpf = models.CharField(max_length=30, verbose_name=u'Cpf', db_column='cpf', unique=True)
    status_account = models.BooleanField(verbose_name=u'Status', default=False, db_column='status_account')
    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', auto_now=True, db_column='updated_at')
    created_at = models.DateTimeField(verbose_name=u'Criado em', auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.cpf

    class Meta:
        verbose_name='Conta'
        verbose_name_plural='Contas'
        ordering=['-created_at']
        db_table='account'
        permissions = (
                ('add_new_account', 'Cadastrar Conta'),
                ('list_new_account', 'Listar Contas'),
                ('delete_new_account', 'Excluir Conta'),
                ('change_new_account', 'Alterar Conta'),
                ('detail_new_account', 'Detalhar Conta'),
        )

class UserManager(models.Manager):

    def list_user(self, user):
        qs = super(UserManager, self).get_queryset()
        if not user.is_superuser:
            qs = qs.none()
        return qs

    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        verbose_name=u'Nome de Usuário', max_length=30,
        validators=[validators.RegexValidator(re.compile('^[\A-Za-z]+$'),
            'O nome de usuário só pode conter letras, digitos ou os '
            'seguintes caracteres: @/./+/-/_', 'invalid')]
    )
    email = models.EmailField(verbose_name=u'E-mail', unique=True)
    is_active = models.BooleanField(verbose_name=u'Está ativo?', default=False)
    is_staff = models.BooleanField(verbose_name=u'É da equipe?', default=False)
    date_joined = models.DateTimeField(verbose_name=u'Data de Entrada', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', auto_now=True, db_column='updated_at')
    account = models.ForeignKey(Account, verbose_name='Conta', related_name='user_account',
                                on_delete=models.CASCADE, null=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return u'%s' % self.email

    def natural_key(self):
        return (self.email)

    @property
    def name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return str(self)

    @models.permalink
    def get_edit_profile(self):
        return ('accounts:edit_profile', {})

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']
        permissions = (
                ('add_new_user', 'Cadastrar Usuários'),
                ('list_new_user', 'Listar Usuários'),
                ('delete_new_user', 'Excluir Usuários'),
                ('change_new_user', 'Alterar Usuários'),
                ('detail_new_user', 'Detalhar Usuários'),
        )



class PasswordReset(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='resets_user',
                             on_delete=models.CASCADE, null=False)
    key = models.CharField(verbose_name=u'Chave', max_length=100, unique=True)
    created_at = models.DateTimeField(verbose_name=u'Criado em', auto_now_add=True)
    confirmed = models.BooleanField(verbose_name=u'Confirmado?', default=False)

    def __unicode__(self):
        return u'%s' % self.user

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']
        permissions = (
                ('add_new_password', 'Cadastrar Senhas'),
                ('list_new_password', 'Listar Senhas'),
                ('delete_new_password', 'Excluir Senhas'),
                ('change_new_password', 'Alterar Senhas'),
                ('detail_new_password', 'Detalhar Senhas'),
        )



class ProfileManager(models.Manager):

    def list_account(self, user):
        qs = super(ProfileManager, self).get_queryset()
        if not user.is_superuser:
            qs = qs.none()
        return qs


class Profile(models.Model):

    ORDER_CHOICE = ((0, 'super'),(1, 'user'))

    id_profile = models.AutoField(primary_key=True, verbose_name=u'id_profile', db_column='id_profile')
    first_name = models.CharField(max_length=50, verbose_name=u'Nome', db_column='first_name',
                                  validators=[validators.RegexValidator(re.compile('^[\A-Za-z]+$'),
                                             'O nome de usuário só pode conter letras', 'invalid')])
    last_name = models.CharField(max_length=100, verbose_name=u'Sobrenome', db_column='last_name')
    status_profile = models.BooleanField(verbose_name=u'Status', default=False, db_column='status_profile')
    state = models.CharField(choices=STATE_CHOICES, max_length=10, verbose_name=u'Estado', db_column='state')
    created_at = models.DateTimeField(verbose_name=u'Data de criação', auto_now_add=True, db_column='date_created')
    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', auto_now=True, db_column='updated_at')
    birthday = models.DateField(verbose_name=u'Aniversario', db_column='birthday', blank=True, null=True)
    url = models.CharField(max_length=100, verbose_name=u'Site', db_column='url', blank=True, null=True)
    description = models.TextField(db_column='description', blank=True, null=True, verbose_name=u'Descricao')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='profile_user',
                                on_delete=models.CASCADE, null=False)
    order = models.IntegerField(choices=ORDER_CHOICE, verbose_name=u'Ordem', db_column='order',
                                default=ORDER_CHOICE[1][0])

    objects = ProfileManager()

    def __unicode__(self):
        return u'%s' % self.first_name

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return str(self)

    @models.permalink
    def active_account(self):
        return ('accounts:active_account', [int(self.pk)], {})

    class Meta:
        verbose_name=u'Profile'
        verbose_name_plural=u'Profile'
        ordering=['-created_at']
        db_table='profile'
        permissions = (
                ('add_new_profile', 'Cadastrar Perfil'),
                ('list_new_profile', 'Listar Perfil'),
                ('delete_new_profile', 'Excluir Perfil'),
                ('change_new_profile', 'Alterar Perfil'),
                ('detail_new_profile', 'Detalhar Perfil'),
        )