#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',)#-*- coding: utf-8 -*-


from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('skripsie.oauth2.client.views',
    (r'^(?P<client_id>\w+)/?$',            'client'),
)# Create your views here.
