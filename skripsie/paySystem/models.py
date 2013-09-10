from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save



#CLAIM_TYPE_CHOICES = [(TICKET, 'Ticket'),(DISCOUNT, 'Discount')]

class Consumer(models.Model):
	
	user_id = models.OneToOneField(User, unique=True, blank=False)
	contactnumber = models.CharField(max_length=12, blank=True)
	acctbalance = models.IntegerField(default=0)
	'''
	class Meta:
		proxy = True
		app_label = 'auth'
		verbose_name = 'Consumer account'
		verbose_name_plural = 'Consumer accounts'
	'''
	def __unicode__(self):
		return unicode(self.user)
	
	def has_efficient_funds(self):
		if(user_acctbalance > 0):
			return True
		else:
			return False

	def user_post_save(sender, instance, created, **kwargs):
		"""Create a user profile when a new user account is created"""
		if created == True:
			user = Consumer()
			user.save()
			user.account = instance
		post_save.connect(user_post_save, sender=User)
	
class Consumer_NFC_Devices(models.Model):
	
	user_id = models.ForeignKey(User, unique=True)
	unfc_id = models.CharField(max_length=20, blank=True)


	
class Claims(models.Model):

	user = models.ForeignKey('auth.User', related_name='claims')
	title = models.CharField(max_length=100, blank=True)
	type = models.CharField(max_length=8, blank=True)
	expiry_date = models.DateTimeField('expiry_date')
	claimed = models.BooleanField(default=False)
	amount = models.IntegerField(default=0)
	
	class Meta:
		ordering = ('expiry_date',)
	
		
	def __unicode__(self):
		return "Title: "+ unicode(self.title) + "\n Type: " + unicode(self.type) +"\n Amount : "+unicode(self.amount) + "\n Expire Date : " + unicode(self.expiry_date) + "\n Claimed : " + unicode(self.claimed)
		
class Transactions(models.Model):
	
	DEBIT = 'DEBT'
	CREDIT = 'CRED'
	TACT_TYPE_CHOICES = ((DEBIT, 'Debit'),(CREDIT,'Credit'))
	tact_datetime = models.DateTimeField('processed date')
	tact_amount = models.IntegerField(default=0)
	tact_debit_credit = models.CharField(max_length=4, choices=TACT_TYPE_CHOICES, default=DEBIT)
	
class Invoices(models.Model):
	
	invc_amount = models.IntegerField(default=0)
	invc_date = models.DateTimeField(auto_now_add=True)

class Vendors(models.Model):
	
	vend_name = models.CharField(max_length=100)
	vend_contactno = models.CharField(max_length=100)
	vend_email = models.CharField(max_length=100)
	vend_acctbal = models.IntegerField(default=0)
	
class Vendors_NFC_Devices(models.Model):
	
	vnfc_id = models.CharField(max_length=10)
	vend_id = models.ForeignKey(Vendors, unique=True)
	