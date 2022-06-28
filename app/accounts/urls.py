#encoding: utf-8

from django.urls import path, reverse_lazy
from accounts.views import (create_account, list_account, 
                            active_account, edit_profile, edit_password, 
                            detail_profile, reset_password, confirm_reset_password,
                            create_user, list_user, edit_user, delete_user, edit_password_user) 
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns=[
    path('sign_in/',LoginView.as_view(template_name='accounts/auth/login.html'), name='login'),
    path('sign_out/',LogoutView.as_view(next_page=reverse_lazy('accounts:login')),name='logout'),
    path('create_account/',create_account, name='create_account'),
    path('list_account/',list_account, name='list_account'),
    path('active_account/<pk>',active_account, name='active_account'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('edit_password/',edit_password, name='edit_password'),
    path('detail_profile/',detail_profile, name='detail_profile'),
    path('reset_password/', reset_password, name='reset_password'),
    path('confirm_reset_password/',confirm_reset_password, name='confirm_reset_password'),
    path('create_user/',create_user, name='create_user'),
    path('list_user/',list_user, name='list_user'),
    path('edit_user/<pk>',edit_user, name='edit_user'),
    path('delete_user/<pk>',delete_user, name='delete_user'),
    path('edit_password_user/<pk>',edit_password_user, name='edit_password_user'),
]