#from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User
from paySystem.models import *
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
	claims = serializers.PrimaryKeyRelatedField(many=True)
	nfcdevices = serializers.PrimaryKeyRelatedField(many=True)		
	invoices = serializers.PrimaryKeyRelatedField(many=True)
	transactions = serializers.PrimaryKeyRelatedField(many=True)
	contactnumber = serializers.CharField(source='userprofile.contactnumber', required=False)
	acct_balance = serializers.IntegerField(source='userprofile.acct_balance')
	acct_available = serializers.IntegerField(source='userprofile.acct_available')
	
	#tags = TagListSerializer(blank=True)
	
	class Meta:
		model = User
		fields = ('id' ,'first_name','last_name','password','email','contactnumber','days_since_joined','acct_balance','acct_available','groups','invoices','transactions','claims','nfcdevices')

	def get_days_since_joined(self, obj):
		return (timezone.now() - obj.date_joined).days	

class NFCDevicesSerializer(serializers.ModelSerializer):
	
	class Meta:
		
		model = NFCDevices
		fields = ('id','username','uid')
	
	pk = serializers.Field()
	username = serializers.Field(source='user.username')
	uid = serializers.CharField(max_length=13, required=True)
		
	def restore_object(self, attrs, instance=None):
		"""
		Create or update a new snippet instance, given a dictionary
		of deserialized field values.
		Note that if we don't define this method, then deserializing
		data will simply return a dictionary of items.
		"""
		if instance:
			# Update existing instance
			instance.username = attrs.get('username', instance.username)
			instance.uid = attrs.get('uid', instance.uid)
			return instance
			
		# Create new instance
		return NFCDevices(**attrs)

class ClaimsSerializer(serializers.ModelSerializer):
	
	class Meta:
		
		model = Claims
		fields = ('id','username','title','type','expiry_date','claimed','amount')
	
	pk = serializers.Field()
	username = serializers.Field(source='user.username')
	title = serializers.CharField(max_length=20, required=False)
	type = serializers.CharField(max_length=6, required=False)
	expiry_date = serializers.DateTimeField('expiry_date')
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
			instance.username = attrs.get('username', instance.username)
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
		fields = ('id','amount_payable','issued_date','transactions')
	
	pk = serializers.Field()
	username = serializers.Field(source='user.username')
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
		of deserialized field values.
		Note that if we don't define this method, then deserializing
		data will simply return a dictionary of items.
		"""
		if instance:
			# Update existing instance
			instance.username = attrs.get('username', instace.username)
			instance.amount_payable = attrs.get('amount_payable', instance.amount_payable)
			instance.issued_date = attrs.get('issued_date', instance.issued_date)
			return instance
			
		# Create new instance
		return Invoices(**attrs)
		
class TransactionsSerializer(serializers.ModelSerializer):
	
	class Meta:
		
		model = Transactions
		fields = ('id','invoice_id','username','processed_date','amount','debit_credit')
		
	pk = serializers.Field()
	invoice_id = serializers.Field()
	username = serializers.Field(source='user.username')
	# processed date
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
			instance.username = attrs.get('username', instance.username)
			instance.invoice_id = attrs.get('invoice_id', instance.invoice_id)
			instance.amount = attrs.get('amount', instance.amount)
			instance.debit_credit = attrs.get('debit_credit', instance.debit_credit)
			return instance
			
		# Create new instance
		return Transactions(**attrs)