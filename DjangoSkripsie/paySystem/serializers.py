#from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User
from paySystem.models import Claims, NFCDevices, UserProfile, Invoices

class UserSerializer(serializers.ModelSerializer):

	claims = serializers.PrimaryKeyRelatedField(many=True)
	nfcdevices = serializers.PrimaryKeyRelatedField(many=True)		
	invoices = serializers.PrimaryKeyRelatedField(many=True)
	contactnumber = serializers.CharField(source='userprofile.contactnumber', required=False)
	acct_balance = serializers.IntegerField(source='userprofile.acct_balance')
	acct_available = serializers.IntegerField(source='userprofile.acct_available')
	
	class Meta:
		model = User
		fields = ('id' ,'first_name','last_name','password','email','contactnumber','date_joined','acct_balance','acct_available','groups','invoices','claims','nfcdevices')


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

class InvoicesSerializer(serializers.ModelSerializer):
	
	class Meta:
		
		model = Invoices
		fields = ('id','username','amount_payable','issued_date')
	
	pk = serializers.Field()
	amount_payable = serializers.IntegerField(required=True)
	issued_date = serializers.DateTimeField()
	
		
	def restore_object(self, attrs, instance=None):
		"""
		Create or update a new snippet instance, given a dictionary
		of deserialized field values.
		Note that if we don't define this method, then deserializing
		data will simply return a dictionary of items.
		"""
		if instance:
			# Update existing instance
			instance.amount_payable = attrs.get('amount_payable', instance.amount_payable)
			instance.issued_date = attrs.get('issued_date', instance.issued_date)
			return instance
			
		# Create new instance
		return Invoices(**attrs)
		
		
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