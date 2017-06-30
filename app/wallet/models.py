#coding: utf-8

from django.db import models
from accounts.models import Account
from django.db.models import Sum
from datetime import datetime



class DebitManager(models.Manager):

    def list_debits(self, user):
        qs = super(DebitManager, self).get_queryset()
        if not user.is_superuser and user.is_active:
            qs = qs.filter(account=user.account)
        elif user.is_superuser:
            qs = qs
        else:
            qs = qs.none()
        return qs

    def sum_debits(self, user):
        qs = super(DebitManager, self).get_queryset()
        if user.is_active:
            qs = qs.filter(account=user.account).aggregate(Sum('value')).get('value__sum') or 0

        return qs


class Debit(models.Model):

    id_debit = models.AutoField(primary_key=True, verbose_name=u'Cod Debit', db_column='id_debit')
    origin = models.CharField(verbose_name=u'Origem', db_column='origin', max_length=30, null=False, blank=False)
    value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=u'Valor', db_column='value',
    							null=False, blank=False)
    document = models.CharField(verbose_name=u'Documento', db_column='document', max_length=30, null=True, blank=True)
    account = models.ForeignKey(Account, verbose_name='Conta', related_name='debits_account',
                                on_delete=models.CASCADE, null=False)
    author = models.CharField(verbose_name=u'Autor', db_column='author', max_length=30, null=False, blank=False)
    date_releases = models.DateTimeField(verbose_name=u'Data do Debito', db_column='date_releases')
    description = models.TextField(db_column='description', blank=True, null=True, verbose_name=u'Descricao')
    created_at = models.DateTimeField(verbose_name=u'Data de criação', auto_now_add=True, db_column='date_created')
    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', auto_now=True, db_column='updated_at')

    objects = DebitManager()

    def __unicode__(self):
        return (u'%s - %s') % (self.origin, self.value)

    @models.permalink
    def get_update_debit(self):
        return ('wallet:update_debit', [int(self.pk)], {})

    @models.permalink
    def get_absolute_url(self):
        return('wallet:detail_debit', [int(self.pk)], {})

    @models.permalink
    def get_delete_debit(self):
        return('wallet:delete_debit', [int(self.pk)], {})

    class Meta:
        verbose_name = 'Debit'
        verbose_name_plural = 'Debit'
        ordering=['-created_at']
        db_table='debit'
        permissions = (
                ('add_new_debit', 'add debit'),
                ('list_new_debit', 'list debit'),
                ('delete_new_debit', 'delete debit'),
                ('change_new_debit', 'change debit'),
                ('detail_new_debit', 'detail debit'),
        )



class DepositManager(models.Manager):

    def list_deposits(self, user):
        qs = super(DepositManager, self).get_queryset()
        if not user.is_superuser and user.is_active:
            qs = qs.filter(account=user.account)
        elif user.is_superuser:
            qs = qs
        else:
            qs = qs.none()
        return qs

    def sum_deposits(self, user):
        qs = super(DepositManager, self).get_queryset()
        if user.is_active:
            qs = qs.filter(account=user.account).aggregate(Sum('value')).get('value__sum') or 0

        return qs


class Deposit(models.Model):

    id_deposit = models.AutoField(primary_key=True, verbose_name=u'Cod Deposit', db_column='id_deposit')
    origin = models.CharField(verbose_name=u'Origem', db_column='origin', max_length=30, null=False, blank=False)
    value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=u'Valor', db_column='value',
                                null=False, blank=False)
    document = models.CharField(verbose_name=u'Documento', db_column='document', max_length=30, null=True, blank=True)
    account = models.ForeignKey(Account, verbose_name='Conta', related_name='deposits_account',
                                on_delete=models.CASCADE, null=False)
    author = models.CharField(verbose_name=u'Autor', db_column='author', max_length=30, null=False, blank=False)
    date_releases = models.DateTimeField(verbose_name=u'Data do Deposito', db_column='date_releases')
    description = models.TextField(db_column='description', blank=True, null=True, verbose_name=u'Descricao')
    created_at = models.DateTimeField(verbose_name=u'Data de criação', auto_now_add=True, db_column='date_created')
    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', auto_now=True, db_column='updated_at')

    objects = DepositManager()

    def __unicode__(self):
        return (u'%s - %s') % (self.origin, self.value)

    @models.permalink
    def get_update_deposit(self):
        return ('wallet:update_deposit', [int(self.pk)], {})

    @models.permalink
    def get_absolute_url(self):
        return('wallet:detail_deposit', [int(self.pk)], {})

    @models.permalink
    def get_delete_deposit(self):
        return('wallet:delete_deposit', [int(self.pk)], {})

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposit'
        ordering=['-created_at']
        db_table='deposit'
        permissions = (
                ('add_new_deposit', 'add deposit'),
                ('list_new_deposit', 'list deposit'),
                ('delete_new_deposit', 'delete deposit'),
                ('change_new_deposit', 'change deposit'),
                ('detail_new_deposit', 'detail deposit'),
        )



class NoteManager(models.Manager):

    def list_notes(self, user):
        qs = super(NoteManager, self).get_queryset()
        if not user.is_superuser and user.is_active:
            qs = qs.filter(account=user.account)
        elif user.is_superuser:
            qs = qs
        else:
            qs = qs.none()
        return qs


class Note(models.Model):

    id_note = models.AutoField(primary_key=True, verbose_name=u'Cod Note', db_column='id_note')
    title = models.CharField(verbose_name=u'TiTulo', db_column='title', max_length=30, null=False, blank=False)
    account = models.ForeignKey(Account, verbose_name='Conta', related_name='notes_account',
                                on_delete=models.CASCADE, null=False)
    author = models.CharField(verbose_name=u'Autor', db_column='author', max_length=30, null=False, blank=False)
    status_alert = models.BooleanField(verbose_name=u'Status Alert', default=False, db_column='status_alert')
    status_note = models.BooleanField(verbose_name=u'Status Note', default=True, db_column='status_note')
    description = models.TextField(db_column='description', blank=True, null=True, verbose_name=u'Descricao')
    date_note = models.DateTimeField(verbose_name=u'Data da Nota', db_column='date_note')
    created_at = models.DateTimeField(verbose_name=u'Data de criação', auto_now_add=True, db_column='date_created')
    updated_at = models.DateTimeField(verbose_name=u'Atualizado em', auto_now=True, db_column='updated_at')

    objects = NoteManager()

    def __unicode__(self):
        return (u'%s - %s') % (self.status_note, self.title)

    @models.permalink
    def get_delete_url(self):
        return('wallet:delete_note', [int(self.pk)], {})

    @models.permalink
    def get_update_url(self):
        return ('wallet:update_note', [int(self.pk)], {})

    @models.permalink
    def get_absolute_url(self):
        return('wallet:detail_note', [int(self.pk)], {})

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Note'
        ordering=['-created_at']
        db_table='note'
        permissions = (
                ('add_new_note', 'add note'),
                ('list_new_note', 'list note'),
                ('delete_new_note', 'delete note'),
                ('change_new_note', 'change note'),
                ('detail_new_note', 'detail note'),
        )