from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
	url(r'^$', RedirectView.as_view(url='/main/',permanent=True), name='index'),
    url(r'^security/', include(admin.site.urls)),
	url(r'^main/', include('main.urls', namespace='main')),
	url(r'^accounts/', include('accounts.urls', namespace='accounts')),
	url(r'^wallet/', include('wallet.urls', namespace='wallet')),
	url(r'^i18n/', include('django.conf.urls.i18n')),
]