from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions

from paySystem.models import Consumer, Consumer_NFC_Devices, Claims, Transactions, Invoices, Vendors, Vendors_NFC_Devices
from paySystem.serializers import ClaimsSerializer, UserSerializer


class UserList(generics.ListAPIView):
	"""
	List all users
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
class UserDetail(APIView):
	"""
	Retreive, update or delete a User instance
	"""
	def get_object(self, username):
		try:
			return User.objects.get(username=username)
		except User.DoesNotExist:
			raise Http404
	
	def get(self, request, username, format=None):
		username = self.get_object(username=username)
		serializer = UserSerializer(username)
		return Response(serializer.data)
	
	def put(self, request, username, format=None):
		user = self.get_object(username=username)
		serializer = SnippetSerializer(user, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, username, format=None):
		user = self.get_object(username=username)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ClaimsList(generics.ListCreateAPIView):
	
	queryset = Claims.objects.all()
	serializer_class = ClaimsSerializer
	
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
		
	def pre_save(self, obj):
		obj.user = self.request.user
	
	"""
    List all snippets, or create a new snippet.
    """
	'''
	def get(self, request, format=None):
		claim = Claims.objects.all()
		serializer = ClaimsSerializer(claim, many=True)
		return Response(serializer.data)
	
	def post(self, request, format=None):
		serializer = ClaimsSerializer(data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
		
class ClaimsDetails(APIView):
		
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
		
	
	def get_object(self, username):
		try:
			user = User.objects.get(username=username)
			return Claims.objects.get(user=user.id)
		except Claims.DoesNotExist:
			raise Http404
	
	def get(self, request, username, format=None):
		claims = self.get_object(username=username)
		serializer = ClaimsSerializer(claims)
		return Response(serializer.data)
		
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
	
class IndexView(generic.ListView):
	template_name = 'paySystem/index.html'
	context_object_name = 'list_of_consumers'
	def get_queryset(self):
	
		return User.objects.all

def profile(request):
	username = request.user
	
	#user_details 
	return HttpResponse("This is %s's profile" % username)
	# try:
		# user = User.objects.get(pk=user_id)
	# except User.DoesNotExist:
		# raise Http404
	# return render(request, 'paySystem/profile.html', {'user': user})
		
def login_user(request):
	state = "Please log in below"
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "You are logged in"
			else:
				state = "Your account is not active"
		
		else:
			state = "Your username and/or password were incorrect"
	
	return render_to_response('login.html', {'state':state, 'username': username})

def logout_user(request):
	logout(request.user)
	
	