from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import url, patterns, include
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns
# The next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from paySystem import views
from paySystem import forms

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
    
	url (r'^$', 																		views.IndexView.as_view()),	
	url (r'^about/',																	views.AboutView.as_view()),
	
	#url(r'^(?P<username>[^/]+)/$',		views.UserDetailsView.as_view()),
	
	
	url (r'^invoice/add',				views.InvoiceCreateView.as_view()),	
	
	url (r'^admin/', 								include(admin.site.urls)),
	url (r'^accounts/', 																include('registration.backends.default.urls')),
	url (r'^accounts/profile/$', views.UserListView.as_view(), name="user_list"),
	
	url (r'^(?P<slug>[\w-]+)/$', views.UserDetailView.as_view(), name="user_detail"),
	url (r'^(?P<slug>[\w-]+)/edit$', views.ProfileUpdateView.as_view(), name="user_profile_edit"),
	url (r'^(?P<slug>[\w-]+)/invoices$',					views.InvoiceListView.as_view(), name="invoices_list"),
	#url (r'^user/settings/account/(?P<slug>[\w-]+)/$', views.MessageAccountUserEdit.as_view(), name="user_account_edit"),
	#url (r'^user/settings/profile/(?P<slug>[\w-]+)/$', views.MessageProfileUserEdit.as_view(), name="user_profile_edit"),
	url (r'^api/', 																		include('rest_framework.urls', namespace='rest_framework')),	
	
	
	url (r'^api/users/$',																views.APIUserList.as_view()),
    url (r'^api/(?P<username>[^/]+)/$', 												views.APIUserDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/claims$', 											views.APIClaimsList.as_view()),
	url (r'^api/(?P<username>[^/]+)/claims/(?P<claim_id>\d+)', 							views.APIClaimsDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/nfcdevices$',										views.APINFCDevicesList.as_view()),
	url (r'^api/(?P<username>[^/]+)/nfcdevices/(?P<nfcdevice_id>\d+)',					views.APINFCDevicesDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/invoices$', 										views.APIInvoicesList.as_view()),
	url (r'^api/(?P<username>[^/]+)/invoices/(?P<invoice_id>\d+)', 						views.APIInvoicesDetails.as_view()),
	url (r'^api/(?P<username>[^/]+)/transactions$',										views.APITransactionsList.as_view()),
	url (r'^api/(?P<username>[^/]+)/transactions/(?P<transact_id>\d+)',					views.APITransactionsDetails.as_view()),
			
	url(r'^google/login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
	url(r'^google/login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
	
	#url(r'^login/$', 'django.contrib.auth.views.login'),
	#url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
	
	url (r'^admin/doc', 							include('django.contrib.admindocs.urls')),
	
	
	url (r'^log/', views.log),
)

urlpatterns = format_suffix_patterns(urlpatterns)