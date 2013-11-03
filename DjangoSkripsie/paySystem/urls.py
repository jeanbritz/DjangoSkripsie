from django.conf.urls import patterns, url


from paySystem import views

urlpatterns = patterns('') + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

