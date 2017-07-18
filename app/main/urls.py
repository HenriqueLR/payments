from django.conf.urls import include, url, patterns

urlpatterns = patterns('main.views',

    url(r'^$','home', name='home'),
    url(r'^graphics/$', 'graphics', name='graphics'),
    url(r'^alerts/$', 'alerts', name='alerts'),
    url(r'^payment/$', 'payment', name='payment'),
    url(r'^balance/$', 'balance', name='balance'),
    url(r'^set_left_menu_session/$', 'set_left_menu_session', name='set_left_menu_session'),
)