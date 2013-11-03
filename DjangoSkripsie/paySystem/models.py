import re
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver



MINIMUM_FUNDS_REQUIRED = 50

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email=None, password=None, **extra_fields):
        now = timezone.now()
		
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(first_name=first_name, last_name=last_name, username=username, email = UserManager.normalize_email(email),
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
	#default profile
	
	username = models.CharField('username', max_length=30, unique=True, db_index=True,
		help_text='Required. 30 characters or fewer. Letters, numbers and '
					'@/./+/-/_ characters',
		validators=[
		validators.RegexValidator(re.compile('^[\w.@+-]+$'), 'Enter a valid username.', 'invalid')
	])
	first_name = models.CharField('First Name', max_length=30, blank=True)
	last_name = models.CharField('Last Name', max_length=30, blank=True)
	contactnumber = models.CharField('Contact Number', max_length=12, blank=True, default="")
	acct_balance = models.IntegerField('Account Balance', default=MINIMUM_FUNDS_REQUIRED)
	acct_available = models.IntegerField('Account Available',default=0)
	email = models.EmailField('Email Address', max_length=254, unique=True)
	date_joined = models.DateTimeField('Date Joined', default=timezone.now)
	location = models.ForeignKey('paySystem.Locations', related_name='location', null=True, default=0)
	
	#user permissions
	is_staff = models.BooleanField('Staff Status', default=False,
		help_text='Designates whether the user can log into this admin site.')
	is_active = models.BooleanField('Active', default=True,
		help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
	
	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Migration:

		needed_by = (
			('authtoken', '0001_initial'),
	)
	
	def __unicode__(self):
		return self.username

	def get_absolute_url(self):
		return reverse('user_profile', args=[self.username])

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name

	def email_user(self, subject, message, from_email=None):
		"""
		Sends an email to this User.
		"""
		send_mail(subject, message, from_email, [self.email])

		
class NFCDevices(models.Model):
	
	user = models.ForeignKey('paySystem.User', related_name='nfcdevices')
	uid = models.CharField(max_length=13, blank=True)
	
	def __unicode__(self):
		return "UID: "+ unicode(self.uid)

	class Meta:
		verbose_name = 'NFCDevice'
		verbose_name_plural = 'NFCDevices'
	
class Claims(models.Model):

	TYPE_CHOICES = (
	('TICKET', 'Ticket'),
	('VOUCHER','Voucher'),
	)
	
	user = models.ForeignKey('paySystem.User', related_name='claims')
	title = models.CharField(_("Title"), max_length=20, blank=False)
	type = models.CharField(_("Type"), max_length=8, choices=TYPE_CHOICES, blank=False)
	expiry_date = models.DateField(_("Expiry Date"), blank=False)
	claimed = models.BooleanField(_("Claimed yet?"), default=False)
	amount = models.IntegerField(_("Amount"), default=0)
	
	class Meta:
		ordering = ('expiry_date',)
		verbose_name = 'Claim'
		verbose_name_plural = 'Claims'
		
	def __unicode__(self):
		return "Title: "+ unicode(self.title) + "\n Type: " + unicode(self.type) +"\n Amount : "+unicode(self.amount) + "\n Expire Date : " + unicode(self.expiry_date) + "\n Claimed : " + unicode(self.claimed)

class Invoices(models.Model):
	
	user = models.ForeignKey('paySystem.User', related_name='invoices')
	amount_payable = models.IntegerField(default=0)
	issued_date = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ('issued_date',)
		verbose_name = 'Invoice'
		verbose_name_plural = 'Invoices'
		
	def __unicode__(self):
		return "[# "+ str(self.id)+ "] - [ "+ self.user.username +" ] "+ "Amount Payable : " + str(self.amount_payable)
		

class Transactions(models.Model):
	
	DEBIT_CREDIT_CHOICES = (
	('DEBIT', 'DEBIT'),
	('CREDIT','CREDIT'),
	)
	
	user = models.ForeignKey('paySystem.User', related_name='transactions')
	invoice = models.ForeignKey('paySystem.Invoices', related_name='transactions')
	processed_date = models.DateTimeField('processed date', auto_now_add=True)
	amount = models.IntegerField(default=0)
	debit_credit = models.CharField(max_length=6, choices=DEBIT_CREDIT_CHOICES, default='DEBIT')
	
	class Meta:
		ordering = ('processed_date',)
		verbose_name = 'Transaction'
		verbose_name_plural = 'Transactions'
	
		
class Locations(models.Model):
	
	NETWORK_CHOICES = (
	('GSM', 'GSM'),
	('WCDMA','WCDMA'),
	('CDMA', 'CDMA'),
	)
	
	caption = models.CharField(max_length=200)
	mcc = models.IntegerField(default=0)
	mnc = models.IntegerField(default=0)
	network = models.CharField(max_length=5, choices=NETWORK_CHOICES, default='GSM')
	lac = models.IntegerField(default=0)
	cell_id = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.caption
	
	class Meta:
		verbose_name = 'Location'
		verbose_name_plural = 'Locations'
	