#encoding: utf-8

from django.conf.urls import patterns, include, url


urlpatterns = patterns('wallet.views',
	url(r'^delete_debit/(?P<pk>\d+)$', 'delete_debit', name='delete_debit'),
	url(r'^detail_debit/(?P<pk>\d+)$', 'detail_debit', name='detail_debit'),
	url(r'^update_debit/(?P<pk>\d+)$', 'update_debit', name='update_debit'),
	url(r'^list_debit/$', 'list_debit', name='list_debit'),
	url(r'^add_debit/$', 'add_debit', name='add_debit'),
)