from django.conf.urls import include, url, patterns

urlpatterns = patterns('main.views',

    url(r'^$','home', name='home'),
    url(r'^graphics/$', 'graphics', name='graphics'),
    url(r'^alerts/$', 'alerts', name='alerts'),
    url(r'^payment/$', 'payment', name='payment'),
    url(r'^list_note/$', 'list_note', name='list_note'),
    url(r'^delete_note/(?P<pk>\d+)$', 'delete_note', name='delete_note'),
    url(r'^list_debit/$', 'list_debit', name='list_debit'),
    url(r'^delete_debit/(?P<pk>\d+)$', 'delete_debit', name='delete_debit'),
    url(r'^list_deposit/$', 'list_deposit', name='list_deposit'),
    url(r'^delete_deposit/(?P<pk>\d+)$', 'delete_deposit', name='delete_deposit'),
    url(r'^balance/$', 'balance', name='balance'),
)