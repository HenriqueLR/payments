#encoding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^sign_in/$','django.contrib.auth.views.login',{'template_name':'accounts/auth/login.html'},name='login'),
    url(r'^sign_out/$','django.contrib.auth.views.logout',{'next_page':'accounts:login'},name='logout'),
    url(r'^create_account/$','accounts.views.create_account',name='create_account'),
    url(r'^list_account/$','accounts.views.list_account',name='list_account'),
    url(r'^active_account/(?P<pk>\d+)$','accounts.views.active_account',name='active_account'),
    url(r'^edit_profile/$','accounts.views.edit_profile',name='edit_profile'),
    url(r'^edit_password/$','accounts.views.edit_password',name='edit_password'),
    url(r'^detail_profile/$','accounts.views.detail_profile',name='detail_profile'),
    url(r'^reset_password/$', 'accounts.views.reset_password', name='reset_password'),
    url(r'^confirm_reset_password/$','accounts.views.confirm_reset_password',name='confirm_reset_password'),
    url(r'^create_user/$','accounts.views.create_user',name='create_user'),
    url(r'^list_user/$','accounts.views.list_user',name='list_user'),
    url(r'^edit_user/(?P<pk>\d+)$','accounts.views.edit_user',name='edit_user'),
    url(r'^delete_user/(?P<pk>\d+)$','accounts.views.delete_user', name='delete_user'),
    url(r'^edit_password_user/(?P<pk>\d+)$','accounts.views.edit_password_user',name='edit_password_user'),
)