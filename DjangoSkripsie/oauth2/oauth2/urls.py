#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
        (r'^missing_redirect_uri/?$',   'skripsie.oauth2.oauth2.views.missing_redirect_uri'),
        (r'^authorize/?$',              'skripsie.oauth2.oauth2.views.authorize'),
        (r'^token/?$',                  'oauth2app.token.handler'),
)