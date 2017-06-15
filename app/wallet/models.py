#encoding: utf-8

from django.db import models
from accounts.models import Account



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


class Debit(models.Model):

    id_debit = models.AutoField(primary_key=True, verbose_name=u'Cod Debit', db_column='id_debit')
    origin = models.CharField(verbose_name=u'Origem', db_column='origin', max_length=30, null=False, blank=False)
    value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=u'Valor', db_column='value',
    							null=False, blank=False)
    document = models.CharField(verbose_name=u'Documento', db_column='document', max_length=30, null=True, blank=True)
    account = models.ForeignKey(Account, verbose_name='Conta', related_name='debits_account',
                                on_delete=models.CASCADE, null=False)
    author = models.CharField(verbose_name=u'Autor', db_column='author', max_length=30, null=False, blank=False)
    description = models.TextField(db_column='description', blank=True, null=True, verbose_name=u'Descricao')
    created_at = models.DateField(verbose_name=u'Data de criação', auto_now_add=True, db_column='date_created')
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
        verbose_name=u'Debit'
        verbose_name_plural=u'Debit'
        ordering=['-created_at']
        db_table='debit'
        permissions = (
                ('add_new_debit', 'add debit'),
                ('list_new_debit', 'list debit'),
                ('delete_new_debit', 'delete debit'),
                ('change_new_debit', 'change debit'),
                ('detail_new_debit', 'detail debit'),
        )