from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from inspector_panel import debug

from paySystem.mixin import *
from paySystem.models import *
from paySystem.serializers import *
from paySystem.forms import *

class APIUserList(generics.ListAPIView):
	"""
	List all users
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
class APIUserDetails(APIView):
	"""
	Retreive, update or delete a User instance
	"""
	def get_object(self, username):
		
		try:
			
			return User.objects.get(username=username)
		
		except User.DoesNotExist:
			raise Http404
		
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

class APIClaimsList(APIView):
	
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
	
		
class APIClaimsDetails(APIView):
		
	def get_object(self, username):
		try:
			user = User.objects.get(username=username)
			return user.claims
		except Claims.DoesNotExist:
			raise Http404
		
	def get(self, request, username, claim_id, format=None):
		
		claims = self.get_object(username=username)
		claim = claims.get(id=claim_id)
		serializer = ClaimsSerializer(claim)
		return Response(serializer.data)
	'''		
	def put(self, request, username, format=None):
		claims = self.get_object(username=username)
		serialize = ClaimsSerializer(claims, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, username, format=None):
		claim = self.get_object(username=username)
		claim.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
	'''
class APINFCDevicesDetails(APIView):
		
	def get_object(self, username):
		try:
			user = User.objects.get(username=username)
			return user.nfcdevices
		except NFCDevices.DoesNotExist:
			raise Http404
	
	def get(self, request, username, nfcdevice_id, format=None):
		nfcdevices = self.get_object(username=username)
		nfcdevice = nfcdevices.get(id=nfcdevice_id)
		serializer = NFCDevicesSerializer(nfcdevice)
		return Response(serializer.data)
	'''	
	def put(self, request, username, format=None):
		nfcdevices = self.get_object(username=username)
		serialize = NFCDevicesSerializer(nfcdevices, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, username, format=None):
		nfcdevices = self.get_object(username=username)
		nfcdevices.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
	'''
class APINFCDevicesList(APIView):
		
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
		
	def put(self, request, username, format=None):
		nfcdevices = self.get_object(username=username)
		serialize = NFCDevicesSerializer(nfcdevices, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, username, format=None):
		nfcdevices = self.get_object(username=username)
		nfcdevices.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
		
class APIInvoicesList(APIView):
	
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

class APIInvoicesDetails(APIView):
		
	def get_object(self, username):
		try:
			user = User.objects.get(username=username)
			return user.invoices
		except Invoices.DoesNotExist:
			raise Http404
	
		
	def get(self, request, username, invoice_id, format=None):
		invoices = self.get_object(username=username)
		invoice = invoices.get(id=invoice_id)
		serializer = InvoicesSerializer(invoice)
		return Response(serializer.data)
	'''	
	def put(self, request, username, format=None):
		invoices = self.get_object(username=username)
		serialize = InvoicesSerializer(invoices, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, username, id, format=None):
		invoice = self.get_object(username=username, id=id)
		invoice.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
	'''
class APITransactionsList(generics.ListAPIView):
	
	def get_object(self, username):
		try:
			user = User.objects.get(username=username)
			return Transactions.objects.filter(user=user.id)
		except Transactions.DoesNotExist:
			raise Http404
	
	def get(self, request, username, format=None):
		transactions = self.get_object(username=username)
		serializer = TransactionsSerializer(transactions)
		return Response(serializer.data)	
		
class APITransactionsDetails(APIView):
	
	def get_object(self, username):
		try:
			user = User.objects.get(username=username)
			return user.transactions
		except Transactions.DoesNotExist:
			raise Http404
	
	def get(self, request, username, transact_id, format=None):
		transactions = self.get_object(username=username)
		transaction = transactions.get(id=transact_id)
		serializer = TransactionsSerializer(transaction)
		return Response(serializer.data)
	'''	
	def put(self, request, username, format=None):
		transactions = self.get_object(username=username)
		serializer = TransactionSerializer(transactions, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, username, format=None):
		transactions = self.get_object(username=username)
		transactions.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
	'''
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
	
class InvoiceCreateView(generic.CreateView):
	model = Invoices
	template_name = 'paySystem/invoices_add.html'
	form_class = InvoiceCreateForm
	success_url = "/"

class AccountUpdateView(LoginRequiredMixin, generic.UpdateView):
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
	def get_queryset(self):
		base_qs = super(ProfileUpdateView, self).get_queryset()
		return base_qs.filter(username=self.request.user.username)

class UserListView(generic.ListView):
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
	slug_field = "username"
	#override the context user object from user to user_profile, use {{ user_profile }} instead of {{ user }} in template
	context_object_name = "user_profile"
	
	


def log (request):
	'''
	content = "<h2>HTTP REQUEST</h2>"
	content += "<p>METHOD: " + request.method + "</p>"
	content += "<p>HOST: " + request.get_host() + "</p>"
	content += "<p>FULL PATH: "+ request.get_full_path() + "</p>"
	content += "<p>PATH: "+ request.path + "</p>"
	content += "<p>BODY: "+ request.body + "</p>"
	#content += "<p>STATUS CODE: "+ request.status_code + "</p>"
	while (request.readline() != ""):
		content += request.readline()
	#content += "<p>CONTENT_LENGTH: "+ request.META['CONTENT_LENGTH'] + "</p>"
	#content += "<p>CONTENT_LENGTH: "+ request.META['CONTENT_LENGTH'] + "</p>"
	
	#request.body = "<h2>Hello</h3>"
	
	f = HttpResponse(content)
	content += "<h2>HTTP RESPONSE</h2>"
	content += "<p>"+f.content+"</p>"
	return HttpResponse(content)
		'''
	d = HttpResponse('<html><body><h3>Test</h3></body></html>');
	debug(d)
	return d
	

	
	