#from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User
from paySystem.models import Consumer, Claims


class UserSerializer(serializers.ModelSerializer):

	claims = serializers.PrimaryKeyRelatedField(many=True)
		
	class Meta:
		model = User
		fields = ('id','username','first_name','last_name','email','groups','claims')
	
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