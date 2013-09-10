from django.conf.urls import patterns, url


from paySystem import views

urlpatterns = patterns('',
    
	
	
	# ex: /paySystem/
	url(r'^$', views.UserDetail.as_view()),
	
	#url(r'^login/', views.LoginView.as_view(), name='login'),
	# ex: /polls/5/
	
)

