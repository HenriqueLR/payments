from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
	path('', RedirectView.as_view(url='/main/',permanent=True), name='index'),
    path('security/', admin.site.urls),
	path('main/', include(('main.urls', 'main'), namespace='main')),
	path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
	path('wallet/', include(('wallet.urls', 'wallet'), namespace='wallet')),
	path('i18n/', include('django.conf.urls.i18n')),
]
