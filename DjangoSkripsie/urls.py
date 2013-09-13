from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import url, patterns, include
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns
# The next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from paySystem import views

''' Start REST Framework Declarations '''
# ViewSets for to define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = User

class GroupViewSet(viewsets.ModelViewSet):
    model = Group

# Routers for provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

''' End REST Framework Declarations '''	

urlpatterns = patterns('',
    
	url (r'^$', 									views.IndexView.as_view()),	
	
	#url (r'^accounts/', 							include('registration.urls')),
	
	url (r'^api/', 								include('rest_framework.urls', namespace='rest_framework')),	
	url (r'^api/claims/$', 							views.ClaimsList.as_view()),
    url (r'^api/(?P<username>[^/]+)/$', 				views.UserDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/claims$', 		views.ClaimsDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/devices$',		views.NFCDevicesDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/invoices$', 		views.InvoicesDetails.as_view()),
	url (r'^api/invoices$', 						views.InvoicesList.as_view()),
	#url(r'^api/(?P<username>[^/]+)', 				include('paySystem.urls', namespace='paySystem')),

	
	url (r'^base$', 							include('skripsie.oauth2.base.urls')),
	url (r'^account/',            				include('skripsie.oauth2.account.urls')),
    url (r'^client$',							include('skripsie.oauth2.client.urls')),
	url (r'^oauth2$',							include('skripsie.oauth2.oauth2.urls')),
    url (r'^api-oauth2$', 							include('skripsie.oauth2.api.urls')),
	
	
	url (r'^admin/doc', 							include('django.contrib.admindocs.urls')),
	url (r'^admin/', 								include(admin.site.urls))
)

urlpatterns = format_suffix_patterns(urlpatterns)