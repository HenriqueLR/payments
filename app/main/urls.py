from django.conf.urls import include, url, patterns

urlpatterns = patterns('main.views',

    url(r'^$','home', name='home'),
    url(r'^graphics/$', 'graphics', name='graphics'),
    url(r'^alerts/$', 'alerts', name='alerts'),
    url(r'^payment/$', 'payment', name='payment'),
    url(r'^list_note/$', 'list_note', name='list_note'),
)