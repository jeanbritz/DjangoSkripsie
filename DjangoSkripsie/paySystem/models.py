import re
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
#from taggit.managers import TaggableManager


MINIMUM_FUNDS_REQUIRED = 50

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(username=username, email = UserManager.normalize_email(email),
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
	gender = models.CharField('Gender',max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
	contactnumber = models.CharField(max_length=12, blank=True, default="")
	acct_balance = models.IntegerField(default=MINIMUM_FUNDS_REQUIRED)
	acct_available = models.IntegerField(default=0)
	email = models.EmailField('email address', max_length=254, unique=True)
	date_joined = models.DateTimeField('date joined', default=timezone.now)
	
	
	#user permissions
	is_staff = models.BooleanField('staff status', default=False,
		help_text='Designates whether the user can log into this admin site.')
	is_active = models.BooleanField('active', default=True,
		help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
	
	is_consumer = models.BooleanField('is consumer', default=False,
		help_text='Designates whether the user is a consumer')
	
	is_vendor = models.BooleanField('is vendor', default=False,
		help_text='Designates whether the user is a vendor') 
	
	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __unicode__(self):
		return _("%s's profile") % self.username

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
	
	user = models.ForeignKey('paySystem.User', related_name='nfcdevices')
	uid = models.CharField(max_length=13, blank=True)
	def __unicode__(self):
		return "UID: "+ unicode(self.uid)

	
class Claims(models.Model):

	user = models.ForeignKey('paySystem.User', related_name='claims')
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
	
	user = models.ForeignKey('paySystem.User', related_name='invoices')
	amount_payable = models.IntegerField(default=0)
	issued_date = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ('issued_date',)
	
	def __unicode__(self):
		return "[# "+ str(self.id)+ "] - [ "+ self.user.username +" ] "+ "Amount Payable : " + str(self.amount_payable)
		

class Transactions(models.Model):
	
	user = models.ForeignKey('paySystem.User', related_name='transactions')
	invoice = models.ForeignKey('paySystem.Invoices', related_name='transactions')
	processed_date = models.DateTimeField('processed date')
	amount = models.IntegerField(default=0)
	debit_credit = models.CharField(max_length=6)
	
	class Meta:
		ordering = ('processed_date',)


	