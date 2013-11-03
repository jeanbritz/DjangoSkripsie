from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import url, patterns, include
from django.contrib.auth.models import Group
from paySystem.models import User
from rest_framework import viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns
# The next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from rest_framework.authtoken.views import obtain_auth_token

from paySystem import views
from paySystem import forms

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

''' Start REST Framework Declarations '''
# ViewSets for to define the view behavior.
#class UserViewSet(viewsets.ModelViewSet):
 #   model = User

#class GroupViewSet(viewsets.ModelViewSet):
#   model = Group

# Routers for provide an easy way of automatically determining the URL conf
#router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
#router.register(r'groups', GroupViewSet)

''' End REST Framework Declarations '''	

urlpatterns = patterns('',
       	
	url (r'^$', 																		views.IndexView.as_view()),	
	url (r'^about/',																	views.AboutView.as_view()),
	url (r'^test/', views.log, name='test'),
	 url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
	 url(r'consumer', views.ConsumerView.as_view(), name="consumer"),
	url(r'^consumer/exchange/',views.ConsumerExchangeView.as_view(), name='consumer-exchange'),
    url(r'^consumer/done/', views.ConsumerDoneView.as_view(), name='consumer-done' ),
    url(r'^consumer/client/',views.TemplateView.as_view(template_name='paySystem/consumer-client.html'),name='consumer-client'),
	
	
	
	
	#url (r'^invoice/add',				views.InvoiceCreateView.as_view()),	
	
	url (r'^admin/', 								include(admin.site.urls)),
	url (r'^accounts/', 																include('registration.backends.default.urls')),
	
	#url (r'^accounts/profile/$', views.UserListView.as_view(), name="user_list"),
	url (r'^location/(?P<slug>\d+)$',				views.LocationDetailView.as_view()),
	
	
	url (r'^api-docs/', include('rest_framework_swagger.urls')),
	url (r'^api/', 																		include('rest_framework.urls', namespace='rest_framework')),	
	
	url (r'^(?P<slug>[^/]+)/$', views.UserDetailView.as_view(), name="user_detail"),
	url (r'^(?P<slug>[^/]+)/edit$', views.ProfileUpdateView.as_view(), name="user_profile_edit"),
		
	url (r'^(?P<slug>[^/]+)/invoices$',					views.InvoiceListView.as_view(), name="invoices_list"),
	url (r'^(?P<slug>[^/]+)/invoices/add$',					views.InvoiceCreateView.as_view(), name="invoices_add"),
	url (r'^invoices/(?P<slug>\d+)/',					views.InvoiceDetailView.as_view(), name="invoices_edit"),
	
	url (r'^(?P<slug>[^/]+)/claims$',					views.ClaimListView.as_view(), name="claims_list"),
	url (r'^(?P<slug>[^/]+)/claims/add$',					views.ClaimCreateView.as_view(), name="claims_add"),
	
	url (r'^(?P<slug>[^/]+)/transactions/$',					views.TransactionListView.as_view(), name="transactions_list"),
	url (r'^(?P<slug>[^/]+)/transactions/add$',					views.TransactionCreateView.as_view(), name="transactions_add"),
		
	url (r'^api/users/$',																views.APIUserList.as_view()),
	url (r'^api/locations/$',															views.APILocationsList.as_view()),
	url (r'^api/locations/(?P<id>\d+)/$',												views.APILocationsDetails.as_view()),
    url (r'^api/(?P<username>[^/]+)/$', 												views.APIUserDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/location$',											views.APILocationsList.as_view()),
	url (r'^api/(?P<username>[^/]+)/claims$', 											views.APIClaimsList.as_view()),
	url (r'^api/claims/(?P<id>\d+)', 													views.APIClaimsDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/nfcdevices$',										views.APINFCDevicesList.as_view()),
	url (r'^api/nfcdevices/(?P<id>\d+)',												views.APINFCDevicesDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/invoices$', 										views.APIInvoicesList.as_view()),
	url (r'^api/invoices/(?P<id>\d+)', 													views.APIInvoicesDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/transactions$',										views.APITransactionsList.as_view()),
	url (r'^api/transactions/(?P<id>\d+)',												views.APITransactionsDetails.as_view()),

	url(r'^arduino/invoice/add', views.ArduinoAddInvoice),
	url(r'^arduino/claim', views.ArduinoCheckClaim),
	url(r'^arduino/payment', views.ArduinoDoPayment),
	
	url(r'^google/login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
	url(r'^google/login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
	
	
	url (r'^admin/doc', 							include('django.contrib.admindocs.urls')),
	
	
	
)

urlpatterns = format_suffix_patterns(urlpatterns)