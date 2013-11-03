from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404, QueryDict
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import *
from django.views.generic import FormView,TemplateView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions, mixins
from inspector_panel import debug

from paySystem.mixin import *
from paySystem.models import *
from paySystem.serializers import *
from paySystem.forms import *
from paySystem.permissions import IsVendor

from oauth2_provider.compat import urlencode
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .forms import ConsumerForm, ConsumerExchangeForm, AccessTokenDataForm

import json
from collections import namedtuple

ApiUrl = namedtuple('ApiUrl', 'name, url')

from datetime import date

class APIUserList(generics.ListAPIView):
	"""
	List all users
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer


class APIUserDetails(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retreive, update or delete a User instance
	"""
	model = User
	serializers_class = UserSerializer
	permission_classes = (permissions.IsAuthenticated, permissions.IsOwner) 
	lookup_field = 'username'
	
	
	
	'''
	def get_object(self, username):
		
		#if self.request.user.username == username:
		try:
			return User.objects.get(username=username)
		
		except User.DoesNotExist:
			raise Http404
		
		#raise Http404
	
	def get(self, request, username, format=None):
		user = self.get_object(username=username)
		serializer = UserSerializer(user)
		return Response(serializer.data)
		
	def put(self, request, username, format=None):
		user = self.get_object(username=username)
		serializer = UserSerializer(user, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, username, format=None):
		user = self.get_object(username=username)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
'''

class APIClaimsList(generics.ListCreateAPIView):
	
	model = Claims
	serializers_class = ClaimsSerializer
	permission_classes = (permissions.IsAuthenticated,) 
	
	
	def get_object(self, username):
		try:
			user = User.objects.get(username=username)
			return Claims.objects.filter(user=user.id)
		except Claims.DoesNotExist:
			raise Http404
	
	def get(self, request, username, format=None):
		claims = self.get_object(username=username)
		serializer = ClaimsSerializer(claims)
		return Response(serializer.data)
		
class APIClaimsDetails(generics.RetrieveUpdateDestroyAPIView):
	
	model = Claims
	serializers_class = ClaimsSerializer
	permission_classes = (permissions.IsAdminUser,) 
	lookup_field = 'id'
	
	
class APINFCDevicesList(generics.ListCreateAPIView):
	"""
    List all NFCDevices, or create a new NFCDevices.
    """
	model = NFCDevices
	serializers_class = NFCDevicesSerializer
	permission_classes = (permissions.IsAuthenticated,) 
	
	def get_object(self, username):
		try:
			user = User.objects.get(username=username)
			return NFCDevices.objects.get(user=user.id)
		except NFCDevices.DoesNotExist:
			raise Http404
        
	def get(self, request, username, format=None):
			nfcdevices = self.get_object(username=username)
			serializer = NFCDevicesSerializer(nfcdevices)
			return Response(serializer.data)
	
class APINFCDevicesDetails(generics.RetrieveUpdateDestroyAPIView):
	
	model = NFCDevices
	serializers_class = NFCDevicesSerializer
	permission_classes = (permissions.IsAuthenticated,) 
	lookup_field = ('id')
	
class APIInvoicesList(generics.ListAPIView):
	
	"""
    List all Invoices, or create a new Invoices.
    """
	model = Invoices
	serializers_class = InvoicesSerializer
	permission_classes = (permissions.IsAuthenticated, IsVendor) 
	
	def get_object(self, username):
		try:
			user = User.objects.get(username=username)
			return Invoices.objects.filter(user=user.id)
		except Invoices.DoesNotExist:
			raise Http404
        
	def get(self, request, username, format=None):
		invoices = self.get_object(username=username)
		serializer = InvoicesSerializer(invoices)
		return Response(serializer.data)
	
	def post(self, request, user_id, amount_payable, format=None):
		invoice = Invoices(user=user_id, amount_payable=amount_payable)
		if (invoice.is_valid()):
			invoice.save()
			serializer = InvoicesSerializer(invoice)
			return Response(serializer.data)
		return Response(serializer.errors)
		
class APIInvoicesDetails(generics.RetrieveUpdateDestroyAPIView):
		
	"""
    View a specific Invoice, edit or delete Invoice.
    """
	model = Invoices
	serializers_class = InvoicesSerializer
	permission_classes = (IsVendor,) 
	lookup_field = ('id')
	
	
class APITransactionsList(generics.GenericAPIView):
	
	model = Transactions
	serializers_class = TransactionsSerializer
	permission_classes = (IsVendor,) 
	
	def get_object(self, username):
		try:
			user = User.objects.get(username=username)
			return user
		except User.DoesNotExist:
			raise Http404
	
	def get(self, request, username, format=None):
		
		user = self.get_object(username=username)
		transactions = Transactions.objects.filter(user=user.id)
		serializer = TransactionsSerializer(transactions)
		return Response(serializer.data)
		
	
	def post(self, request, username, format=None):
		
		consumer = User.objects.get(id=request.DATA['user'][:]) # the user who this transaction is meant for
		vendor = self.get_object(username=username) # The user that is logged in
		
		if consumer != vendor:
		
			if request.DATA['debit_credit'] == "DEBIT":
			
				amount = int(request.DATA['amount'][:])
			
				if amount <= consumer.acct_balance:
				
					# Amount is subtracted (debited) from consumer
					new_balance = consumer.acct_balance - amount
					consumer.acct_balance = new_balance
					
					
					# Amount is added (credited) to vendor
					new_balance = vendor.acct_balance + amount
					vendor.acct_balance = new_balance
					
					# Make an entry of the debit transaction
					serializer = TransactionsSerializer(data=request.DATA)
					debug(serializer.data)
					if serializer.is_valid():
						consumer.save()
						vendor.save()
						serializer.save()
						return Response(serializer.data, status=status.HTTP_201_CREATED)
					else:
						return Response(serializer.errors, status=status.HTTP_206_PARTIAL_CONTENT)
					
				else:
					return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
				
		
	
class APITransactionsDetails(generics.RetrieveUpdateDestroyAPIView):
	model = Transactions
	serializers_class = TransactionsSerializer
	permission_classes = (IsVendor,) 
	lookup_field = ('id')
	
class APILocationsList(generics.ListAPIView):
	
	model = Locations
	serializers_class = LocationsSerializer
	permission_classes = (permissions.IsAuthenticated,) 
		
	def get_object(self):
		try:
			
			return Locations.objects.all()
		except Locations.DoesNotExist:
			raise Http404
	
	def get(self, request, format=None):
		locations = self.get_object()
		serializer = LocationsSerializer(locations)
		return Response(serializer.data, status=status.HTTP_200_OK)	
	
class APILocationsDetails(generics.RetrieveUpdateDestroyAPIView):
	
	model = Locations
	serializers_class = LocationsSerializer
	permission_classes = (permissions.IsAuthenticated,) 
	lookup_field = ('id')

	
class IndexView(generic.ListView):
	model = User
	template_name = 'paySystem/index.html'
		
class AboutView(TemplateView):
	template_name = 'paySystem/about.html'

class InvoiceListView(LoginRequiredMixin, generic.ListView):
	template_name = 'paySystem/invoices_list.html'
	paginate_by = 10
	context_object_name = 'invoices_list'
	slug_field = "username"
	def get_queryset(self):
		return Invoices.objects.filter(user=self.request.user)

class InvoiceDetailView(LoginRequiredMixin, generic.DetailView):
	"""
	Class to display invoice in detail
	"""
	model = Invoices
	template_name = 'paySystem/invoices_detail.html'
	context_object_name = 'invoice'
	slug_field = 'id'
		
class InvoiceCreateView(LoginRequiredMixin, generic.CreateView):
	model = Invoices
	template_name = 'paySystem/invoices_add.html'
	form_class = InvoiceCreateForm
	success_url = "./"

class InvoiceUpdateView(LoginRequiredMixin, generic.UpdateView):
	model = Invoices
	form_class = InvoiceCreateForm
	template_name = 'paySystem/invoices_edit.html'
	success_url = "./"	
	slug_field='id'
	def get_queryset(self):
		base_qs = super(ProfileUpdateView, self).get_queryset()
		return base_qs.filter(username=self.request.user.username)

class ClaimListView(LoginRequiredMixin, generic.ListView):
	template_name = 'paySystem/claims_list.html'
	paginate_by = 10
	context_object_name = 'claims_list'
	slug_field = "username"
	def get_queryset(self):
		return Claims.objects.filter(user=self.request.user)

class ClaimCreateView(generic.CreateView):
	model = Claims
	template_name = 'paySystem/claims_add.html'
	form_class = ClaimCreateForm
	success_url = "."

class TransactionListView(generic.ListView):
	template_name = 'paySystem/tranactions_list.html'
	paginate_by = 10
	context_object_name = 'transactions_list'
	slug_field = "username"
	def get_queryset(self):
		return Transactions.objects.filter(user=self.request.user)

class TransactionCreateView(generic.CreateView):
	
	template_name = 'paySystem/transactions_add.html'
	form_class = TransactionCreateForm
	success_url = "./"
	
class LocationDetailView(generic.DetailView):
	"""
	Class to display location in detail
	"""
	model = Locations
	template_name = 'paySystem/location_detail.html'
	context_object_name = 'location'
	slug_field = 'id'
		
class AccountUpdateView(generic.UpdateView):
	"""
	Class that only allows authentic user to update their account
	username, email
	"""
	model = User
	form_class = AccountForm
	template_name = "paySystem/user_account_edit.html"
	success_url = "."
	slug_field = "username"
	def get_queryset(self):
		base_qs = super(ProfileUpdateView, self).get_queryset()
		return base_qs.filter(username=self.request.user.username)

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
	"""
	Class that only allows authentic user to update their profile
	Composed of first_name,last_name,date_of_birth,gender,
	"""
	model = User
	form_class = ProfileForm
	template_name = "paySystem/user_profile_edit.html"
	success_url = "."
	slug_field = "username"
	#def get_queryset(self):
	#	base_qs = super(ProfileUpdateView, self).get_queryset()
	#	return base_qs.filter(username=self.request.user.username)

class UserListView(LoginRequiredMixin, generic.ListView):
	"""
	Class to list all the user
	"""
	model = User
	template_name = "paySystem/user_list.html"
	context_object_name = "users"

class UserDetailView(generic.DetailView):
	"""
	Class to display user profile in detail
	"""
	model = User
	template_name = "paySystem/user_detail.html"
	#use username instead of pk
	slug_field = 'username'
	#override the context user object from user to user_profile, use {{ user_profile }} instead of {{ user }} in template
	context_object_name = "user_profile"
	
	


def log (request): 
	return HttpResponse('<html><body><h3>Test</h3></body></html>');

@csrf_exempt	
def ArduinoAddInvoice(request):
	if request.method == "POST":
		
		form = ArduinoAddForm(request.POST)				
		if form.is_valid():
			form.save()
			
			return HttpResponse('V') # Valid / Created
		return HttpResponse(form.errors)
	if request.method == "GET":
				
		return HttpResponse('Arduino Usage')

def ArduinoCheckClaim(request):
	if request.method == "GET":
		claim = Claims.objects.get(id=request.GET['id'], user=request.GET['user'])
		if claim.claimed == False:
			if date.today() < claim.expiry_date:
				claim.claimed = True
				claim.save()
				return HttpResponse('V') # Valid
					
	return HttpResponse('E') # Expired

def ArduinoDoPayment(request):
	
	vendor = User.objects.get(username="jannie.vendor") # The 'Vendor'
	
	if(request.method == "POST"):
		
		
		consumer = get_consumer(request) # the user who this transaction is meant for
		
		cons_acct = consumer.acct_available
		transact_value = request.POST['amount'][:]
		invoice_id = request.POST['invoice_id'][:]
		if(cons_acct >= transact_value):
			new_acct_val = consumer.acct_available - transact_value
			consumer.acct_available = new_acct_val
			consumer.save()
			new_acct_val = vendor.acct_available + transact_val
			vendor.acct_available = new_acct_val
			vendor.save()
			transact_cons = Transactions(invoice_id = invoice_id, user=consumer.id, amount=transact_value, debit_credit="Debit")
			transact_vendor = Transactions(invoice_id = invoice_id, user=consumer.id, amount=transact_value, debit_credit="Credit")
			transact_cons.save();
			transact_vendor.save();
			return HttpResponse('V') # Valid/Accepted
		return HttpResponse('E') # Not enough funds
	return HttpResponse('Arduino Usage')
	

def get_consumer(request):
	try:
		return Locations.objects.filter(id=request.POST['user_id'][:])
	except Locations.DoesNotExist:
		raise HttpResponse('N') # Does not exist	

class ConsumerExchangeView(FormView):
    """
The exchange view shows a form to manually perform the auth token swap
"""
    form_class = ConsumerExchangeForm
    template_name = 'paySystem/consumer-exchange.html'

    def get(self, request, *args, **kwargs):
        try:
            self.initial = {
                'code': request.GET['code'],
                'state': request.GET['state'],
                'redirect_url': request.build_absolute_uri(reverse('consumer-exchange'))
            }
        except KeyError:
            kwargs['noparams'] = True

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form, **kwargs))


class ConsumerView(FormView):
    """
The homepage to access Consumer's functionalities in the case of Authorization Code flow.
It offers a form useful for building "authorization links"
"""
    form_class = ConsumerForm
    success_url = '/consumer/'
    template_name = 'paySystem/consumer.html'

    def __init__(self, **kwargs):
        self.authorization_link = None
        super(ConsumerView, self).__init__(**kwargs)

    def get_success_url(self):
        url = super(ConsumerView, self).get_success_url()
        return '{url}?{qs}'.format(url=url, qs=urlencode({'authorization_link': self.authorization_link}))

    def get(self, request, *args, **kwargs):
        kwargs['authorization_link'] = request.GET.get('authorization_link', None)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form, **kwargs))

    def post(self, request, *args, **kwargs):
        self.request = request
        return super(ConsumerView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        qs = urlencode({
            'client_id': form.cleaned_data['client_id'],
            'response_type': 'code',
            'state': 'random_state_string',
        })
        self.authorization_link = "{url}?{qs}".format(url=form.cleaned_data['authorization_url'], qs=qs)
        return super(ConsumerView, self).form_valid(form)


class ConsumerDoneView(TemplateView):
    """
If exchange succeeded, come here, show a token and let users use the refresh token
"""
    template_name = 'example/consumer-done.html'

    def get(self, request, *args, **kwargs):
        # do not show form when url is accessed without paramters
        if 'access_token' in request.GET:
            form = AccessTokenDataForm(initial={
                'access_token': request.GET.get('access_token', None),
                'token_type': request.GET.get('token_type', None),
                'expires_in': request.GET.get('expires_in', None),
                'refresh_token': request.GET.get('refresh_token', None),
            })
            kwargs['form'] = form

        return super(ConsumerDoneView, self).get(request, *args, **kwargs)


class ApiClientView(TemplateView):
    """
TODO
"""
    template_name = 'example/api-client.html'

    def get(self, request, *args, **kwargs):
        from .urls import urlpatterns
        endpoints = []
        for u in urlpatterns:
            if 'api/' in u.regex.pattern:
                endpoints.append(ApiUrl(name=u.name, url=reverse(u.name,
                                                                 args=u.regex.groupindex.keys())))
        kwargs['endpoints'] = endpoints
        return super(ApiClientView, self).get(request, *args, **kwargs)


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')
