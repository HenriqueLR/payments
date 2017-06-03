#encoding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^sign_in/$','django.contrib.auth.views.login', {'template_name':'accounts/auth/login.html'}, name='login'),
    url(r'^sign_out/$','django.contrib.auth.views.logout', {'next_page':'accounts:login'}, name='logout'),
    url(r'^create_account/$','accounts.views.create_account', name='create_account'),
    url(r'^list_account/$','accounts.views.list_account', name='list_account'),
    url(r'^active_account/(?P<pk>\d+)$', 'accounts.views.active_account', name='active_account'),
    url(r'^edit_profile/$','accounts.views.edit_profile', name='edit_profile'),
    url(r'^edit_password/$','accounts.views.edit_password', name='edit_password'),
)