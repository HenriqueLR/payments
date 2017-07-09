#encoding: utf-8

from django.conf.urls import patterns, include, url


urlpatterns = patterns('wallet.views',
	#debit urls
	url(r'^delete_debit/(?P<pk>\d+)$', 'delete_debit', name='delete_debit'),
	url(r'^detail_debit/(?P<pk>\d+)$', 'detail_debit', name='detail_debit'),
	url(r'^update_debit/(?P<pk>\d+)$', 'update_debit', name='update_debit'),
	url(r'^list_debit/$', 'list_debit', name='list_debit'),
	url(r'^add_debit/$', 'add_debit', name='add_debit'),

	#deposit urls
	url(r'^delete_deposit/(?P<pk>\d+)$', 'delete_deposit', name='delete_deposit'),
	url(r'^detail_deposit/(?P<pk>\d+)$', 'detail_deposit', name='detail_deposit'),
	url(r'^update_deposit/(?P<pk>\d+)$', 'update_deposit', name='update_deposit'),
	url(r'^list_deposit/$', 'list_deposit', name='list_deposit'),
	url(r'^add_deposit/$', 'add_deposit', name='add_deposit'),

	#note urls
	url(r'^delete_note/(?P<pk>\d+)$', 'delete_note', name='delete_note'),
	url(r'^detail_note/(?P<pk>\d+)$', 'detail_note', name='detail_note'),
	url(r'^update_note/(?P<pk>\d+)$', 'update_note', name='update_note'),
	url(r'^list_note/$', 'list_note', name='list_note'),
	url(r'^add_note/$', 'add_note', name='add_note'),
	url(r'^update_status_note/(?P<pk>\d+)$', 'update_status_note', name='update_status_note'),
)