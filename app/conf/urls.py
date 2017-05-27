from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    url(r'^security/', include(admin.site.urls)),
]