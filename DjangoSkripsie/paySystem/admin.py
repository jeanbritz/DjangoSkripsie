from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User
from django.db.models import Q
from paySystem.models import *


'''
class ClaimsInline(admin.TabularInline):
	model = Claims
	can_delete = True
	date_hierarchy = ''
	list_select_related = True
	verbose_name = 'Claim'
	verbose_name_plural = 'Claims'
'''
'''	

class ConsumerInline(admin.TabularInline):
	model = Consumer
	can_delete = False
	verbose_name_plural = 'consumers'
'''

admin.site.register(User)
admin.site.register(Claims)
admin.site.register(Invoices)
admin.site.register(Transactions)

#admin.site.register(Consumer, ConsumerAdmin)