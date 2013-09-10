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
    url(r'^$', views.IndexView.as_view()),	
	url(r'^login/$', 'django.contrib.auth.views.login'),
	#url(r'^accounts/profile/$', 'paySystem.views.profile'),
	#url(r'^$', include('registration.backends.default.urls', namespace="registration")),
	
	url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),	
	url(r'^api/claims/$', views.ClaimsList.as_view()),
    #url(r'^api/claims/(?P<pk>[0-9]+)/$', views.ClaimsDetails().as_view()),
	url(r'^api/(?P<username>[^/]+)/$', views.UserDetail.as_view()),
	url(r'^api/(?P<username>[^/]+)/claims$', views.ClaimsDetails.as_view()),
	#url(r'^api/(?P<username>[^/]+)', include('paySystem.urls', namespace='paySystem')),
	
	
	
	#url(r'^admin/doc$', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls))
)

urlpatterns = format_suffix_patterns(urlpatterns)