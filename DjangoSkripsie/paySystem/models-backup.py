from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
#from taggit.managers import TaggableManager


MINIMUM_FUNDS_REQUIRED = 50

class UserProfile(models.Model):

	user = models.OneToOneField(User)
	contactnumber = models.CharField(max_length=12, blank=True, default="")
	acct_balance = models.IntegerField(default=MINIMUM_FUNDS_REQUIRED)
	acct_available = models.IntegerField(default=0)
	
	#tags = TaggableManager(blank=True)
	
	def __unicode__(self):
		return "%s\'s profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

class NFCDevices(models.Model):
	
	user = models.ForeignKey('auth.User', related_name='nfcdevices')
	uid = models.CharField(max_length=13, blank=True)
	def __unicode__(self):
		return "UID: "+ unicode(self.uid)

	
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

class Invoices(models.Model):
	
	user = models.ForeignKey('auth.User', related_name='invoices')
	amount_payable = models.IntegerField(default=0)
	issued_date = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ('issued_date',)
	
	def __unicode__(self):
		return "[# "+ str(self.id)+ "] - [ "+ self.user.username +" ] "+ "Amount Payable : " + str(self.amount_payable)
		

class Transactions(models.Model):
	
	user = models.ForeignKey('auth.User', related_name='transactions')
	invoice = models.ForeignKey('Invoices', related_name='transactions')
	processed_date = models.DateTimeField('processed date')
	amount = models.IntegerField(default=0)
	debit_credit = models.CharField(max_length=6)
	
	class Meta:
		ordering = ('processed_date',)


	