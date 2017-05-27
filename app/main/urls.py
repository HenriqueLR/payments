from django.conf.urls import include, url, patterns

urlpatterns = patterns('main.views',

    url(r'^$','home', name='home'),
)