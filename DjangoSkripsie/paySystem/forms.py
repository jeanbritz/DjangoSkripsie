from django.forms import *
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

from paySystem.models import *

from inspector_panel import debug

"""
Forms and validation code for user profile.
"""
class AccountForm(ModelForm):

    class Meta:
        model = User
        #fields = ('username', 'email')

class ProfileForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','contactnumber','location')
	
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
	
		
class InvoiceCreateForm(ModelForm):
	
	class Meta:
		model = Invoices
	
	def __init__(self, *args, **kwargs):
		super(InvoiceCreateForm, self).__init__(*args, **kwargs)
		
		#text_input = forms.CharField()
		# If you pass FormHelper constructor a form instance
		# It builds a default layout with all its fields
		self.helper = FormHelper(self)
		self.form_class= 'form-horizontal'
		
		# You can dynamically adjust your layout
		#self.helper.layout = Layout (
		#	Field('text_input', css_class='input_large'),
		#	)
		self.helper.layout.append(Submit('Create', 'Create', css_class="btn-primary"))
		#self.helpet.layout.append(HTML("a class='btn' href='{% url ..\" %}'>Back")

class InvoiceUpdateForm(ModelForm):
	
	class Meta:
		model = Invoices
	
	def __init__(self, *args, **kwargs):
		super(InvoiceCreateForm, self).__init__(*args, **kwargs)
		
		#text_input = forms.CharField()
		# If you pass FormHelper constructor a form instance
		# It builds a default layout with all its fields
		self.helper = FormHelper(self)
		self.form_class= 'form-horizontal'
		
		# You can dynamically adjust your layout
		#self.helper.layout = Layout (
		#	Field('text_input', css_class='input_large'),
		#	)

class ClaimCreateForm(ModelForm):
	
	class Meta:
		model = Claims
	
	def __init__(self, *args, **kwargs):
		super(ClaimCreateForm, self).__init__(*args, **kwargs)
		
		#text_input = forms.CharField()
		# If you pass FormHelper constructor a form instance
		# It builds a default layout with all its fields
		self.helper = FormHelper(self)
		self.form_class= 'form-horizontal'
		
		# You can dynamically adjust your layout
		#self.helper.layout = Layout (
		#	Field('text_input', css_class='input_large'),
		#	)
		self.helper.layout.append(Submit('Create', 'Create', css_class="btn-primary"))
		#self.helpet.layout.append(HTML("a class='btn' href='{% url ..\" %}'>Back")		

class TransactionCreateForm(ModelForm):
	
	class Meta:
		model = Transactions
		fields = ('user', 'invoice', 'amount','debit_credit',)
	
	def __init__(self, *args, **kwargs):
		
		super(TransactionCreateForm, self).__init__(*args, **kwargs)
		
		#text_input = forms.CharField()
		# If you pass FormHelper constructor a form instance
		# It builds a default layout with all its fields
		self.helper = FormHelper(self)
		self.form_class= 'form-horizontal'
		
		# You can dynamically adjust your layout
		#self.helper.layout = Layout (
		#	Field('text_input', css_class='input_large'),
		#	)
		self.helper.layout.append(Submit('Create', 'Create', css_class="btn-primary"))
		#self.helpet.layout.append(HTML("a class='btn' href='{% url ..\" %}'>Back")
	
			
			
class ArduinoAddForm(ModelForm):			
	
	class Meta:
		model = Invoices
		fields = ['user','amount_payable']

class ConsumerForm(forms.Form):
    client_id = forms.CharField()
    authorization_url = forms.URLField()


class ConsumerExchangeForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    token_url = forms.URLField()
    grant_type = forms.CharField(widget=forms.HiddenInput(), initial='authorization_code')
    redirect_url = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    client_id = forms.CharField()
    client_secret = forms.CharField()


class AccessTokenDataForm(forms.Form):
    access_token = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    token_type = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    expires_in = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    refresh_token = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    token_url = forms.URLField()
    client_id = forms.CharField()
    client_secret = forms.CharField()
	
	