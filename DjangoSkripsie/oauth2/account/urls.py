#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('skripsie.oauth2.account.views',
    url(r'^login',                  	'login'),
    url(r'^logout',                	'logout'),
    url(r'^signup',                	'signup'),
    url(r'^clients',               	'clients'),
)