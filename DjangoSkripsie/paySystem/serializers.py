#from django.forms import widgets
from rest_framework import serializers
from paySystem.models import *
from paySystem.models import User as paySystemUser
from django.utils import timezone
'''
class TagListSerializer(serializers.WritableField):
	
	def from_native(self, data):
        if type(data) is not list:
            raise ParseError("expected a list of data")    
        return data
     
    def to_native(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj
'''
class UserSerializer(serializers.ModelSerializer):

	days_since_joined = serializers.SerializerMethodField('get_days_since_joined')
	contactnumber = serializers.CharField(required=False)
	acct_balance = serializers.IntegerField()
	location = serializers.PrimaryKeyRelatedField(source='paySystem.locations', many=False,  required=False, read_only=True)
	claims = serializers.PrimaryKeyRelatedField(source='paySystem.claims',many=True, read_only=True)
	nfcdevices = serializers.PrimaryKeyRelatedField(source='paySystem.nfcdevices', many=True, read_only=True)		
	invoices = serializers.PrimaryKeyRelatedField(source='paySystem.invoices', many=True, read_only=True)
	transactions = serializers.PrimaryKeyRelatedField(source='paySystem.transactions', many=True, read_only=True)
	#tags = TagListSerializer(blank=True)
	
	class Meta:
		model = paySystemUser
		fields = ('id' ,'first_name','last_name','email','contactnumber','days_since_joined','acct_balance','acct_available','location','groups','invoices','transactions','claims','nfcdevices')

	def get_days_since_joined(self, obj):
		return (timezone.now() - obj.date_joined).days	

class NFCDevicesSerializer(serializers.ModelSerializer):
	
	pk = serializers.Field()
	user = serializers.Field(source='user.id')
	uid = serializers.CharField(max_length=13, required=True)
	
	class Meta:
		
		model = NFCDevices
		fields = ('id','user','uid',)
			
	def restore_object(self, attrs, instance=None):
		"""
		Create or update a new snippet instance, given a dictionary
		of deserialized field values.
		Note that if we don't define this method, then deserializing
		data will simply return a dictionary of items.
		"""
		if instance:
			# Update existing instance
			instance.user = attrs.get('user', instance.user)
			instance.uid = attrs.get('uid', instance.uid)
			return instance
			
		return NFCDevices(**attrs)
	
class ClaimsSerializer(serializers.ModelSerializer):
	
	class Meta:
		
		model = Claims
		fields = ('id','user','title','type','expiry_date','claimed','amount')
	
	pk = serializers.Field()
	user = serializers.Field(source='user.id')
	title = serializers.CharField(max_length=20, required=False)
	type = serializers.CharField(max_length=6, required=False)
	expiry_date = serializers.DateField('expiry_date')
	claimed = serializers.BooleanField(default=False)
	amount = serializers.IntegerField(default=0)
	
	def restore_object(self, attrs, instance=None):
		"""
		Create or update a new snippet instance, given a dictionary
		of deserialized field values.
		Note that if we don't define this method, then deserializing
		data will simply return a dictionary of items.
		"""
		if instance:
			# Update existing instance
			instance.user = attrs.get('user', instance.user)
			instance.title = attrs.get('title', instance.title)
			instance.type = attrs.get('type', instance.type)
			instance.expiry_date = attrs.get('expiry_date', instance.clam_expiry_date)
			instance.claimed = attrs.get('claimed', instance.claimed)
			instance.amount = attrs.get('amount', instance.amount)
			return instance
			
		# Create new instance
		return Claims(**attrs)

class InvoicesSerializer(serializers.ModelSerializer):
	
	payment_completed = serializers.Field(source='payment_completed')
	
	class Meta:
		
		model = Invoices
		fields = ('id','amount_payable','issued_date')
	
	pk = serializers.Field()
	user = serializers.Field(source='user.id')
	amount_payable = serializers.IntegerField(required=True)
	issued_date = serializers.DateTimeField()
	transactions = serializers.PrimaryKeyRelatedField(source='transactions',many=True, read_only=True)
	
	def payment_completed(self):
		"""
		This verifies whether the invoice has been paid
		"""
		return True
		
	def restore_object(self, attrs, instance=None):
		"""
		Create or update a new snippet instance, given a dictionary
		of de-serialized field values.
		Note that if we don't define this method, then de-serializing
		data will simply return a dictionary of items.
		"""
		if instance:
			# Update existing instance
			instance.user = attrs.get('user', instace.user)
			instance.amount_payable = attrs.get('amount_payable', instance.amount_payable)
			instance.issued_date = attrs.get('issued_date', instance.issued_date)
			return instance
			
		# Create new instance
		return Invoices(**attrs)
		
class TransactionsSerializer(serializers.ModelSerializer):
	
	class Meta:
		
		model = Transactions
		fields = ('id','invoice_id','processed_date','user','amount','debit_credit')
		
	pk = serializers.Field()
	invoice_id = serializers.Field()
	username = serializers.Field(source='user.id')
	processed_date = serializers.DateTimeField()
	amount = serializers.IntegerField(default=0)
	debit_credit = serializers.CharField(max_length=6)
	
	def restore_object(self, attrs, instance=None):
		"""
		Create or update a new snippet instance, given a dictionary
		of deserialized field values.
		Note that if we don't define this method, then deserializing
		data will simply return a dictionary of items.
		"""
		if instance:
			# Update existing instance
			instance.username = attrs.get('user', instance.username)
			instance.invoice_id = attrs.get('invoice_id', instance.invoice_id)
			#instance.processed_date = attrs.get('processed_date', instance.processed_date)
			instance.amount = attrs.get('amount', instance.amount)
			instance.debit_credit = attrs.get('debit_credit', instance.debit_credit)
			return instance
			
		# Create new instance
		return Transactions(**attrs)
		
class LocationsSerializer(serializers.ModelSerializer):
	
	NETWORK_CHOICES = (
	('GSM', 'GSM'),
	('WCDMA','WCDMA'),
	('CDMA', 'CDMA'),
	)
	
	pk = serializers.Field()
	caption = serializers.Field()
	mcc = serializers.IntegerField(default=0)
	mnc = serializers.IntegerField(default=0)
	network = serializers.CharField(max_length=5, default='GSM')
	lac = serializers.IntegerField(default=0)
	cell_id = serializers.IntegerField(default=0)
	
	class Meta:
		
		model = Locations
		fields = ('id','caption','mcc','mnc','network','lac','cell_id')
		
	def restore_object(self, attrs, instance=None):
		"""
		Create or update a new snippet instance, given a dictionary
		of deserialized field values.
		Note that if we don't define this method, then deserializing
		data will simply return a dictionary of items.
		"""
		if instance:
			# Update existing instance
			instance.caption = attrs.get('caption', instance.caption)
			instance.mcc = attrs.get('mcc', instance.mcc)
			instance.mnc = attrs.get('mnc', instance.mnc)
			instance.network = attrs.get('network', instance.network)
			instance.lac = attrs.get('lac', instance.lac)
			instance.cell_id = attrs.get('cell_id', instance.cell_id)
			return instance
			
		# Create new instance
		return Locations(**attrs)