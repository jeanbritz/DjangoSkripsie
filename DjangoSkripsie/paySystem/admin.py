from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Q

#from paySystem.models import Consumer


'''
class ConsumerInline(admin.TabularInline):
	model = Consumer
	can_delete = False
	verbose_name_plural = 'consumers'
'''
'''	
class SuperUserAdmin(UserAdmin):
	inlines = (ConsumerInline,)
	
	class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Staff account'
        verbose_name_plural = 'Staff accounts'
	
	def queryset(self, request):
		qs = super(UserAdmin, self).queryset(request)
		qs = qs.filter(Q(is_staff=True) | Q(is_superuser=True))
		return qs
'''
'''
class ConsumerAdmin(SuperUserAdmin):
	
	def queryset(self, request):
		qs = super(SuperUserAdmin, self).queryset(request)
		qs = qs.exclude(Q(is_staff=True) | Q(is_superuser=True))
		return qs
'''	
#admin.site.unregister(User)
#admin.site.register(User, SuperUserAdmin)
#admin.site.register(Consumer, ConsumerAdmin)