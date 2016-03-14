from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import messages
import sys
# from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
import datetime
from django.shortcuts import redirect
from user.forms import LoginForm, SignupForm

def signup(request):
	try:
		args={}
		form = SignupForm()
		if request.method == 'POST':
			form = SignupForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				email = cd['email']
				username = cd['username']
				password = cd['password']
				confirm = cd['confirm']
				result = User.objects.create_user(password=password, username=username, first_name="", last_name="", email=email)
				if result:
					messages.add_message(request, messages.INFO, "Welcome, You are Registered Successfully.")
					return HttpResponseRedirect('/items/')	
				else:
					messages.add_message(request, messages.ERROR, "Error occured during registration. Please Try Again.")
					return render(request, 'user/signup.html')
			else:
				args['form'] = form	
				return render(request, 'user/signup.html', args)
		else:
			return render(request, 'user/signup.html', {'form':form})
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
	return render(request, 'user/signup.html', {'form':form})

def login_account(request):
	try:
		args={}
		form = LoginForm()
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				username = cd['username']
				password = cd['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:	
						# update last login in database
						result = User.objects.filter(username=username).update(last_login=datetime.datetime.now())
						login(request, user) #Django buildin login method
						# request.session['bookserviceUser'] = username
						# response = HttpResponse()
						# response.set_cookie('bookserviceLogin', 'True')
						return HttpResponseRedirect('/items/')
					else:
						messages.add_message(request, messages.INFO, 'This account has been disabled.')
				else:
					messages.add_message(request, messages.INFO, 'Invalid Username and Password')
			else:
				args['form'] = form	
				return render(request, 'user/login.html', args)
		else:
			return render(request, 'user/login.html', {'form':form})
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
	return render(request, 'user/login.html', {'form':form})

def logout_account(request):
	try:
		# del request.session['bookserviceUser']
		# response = HttpResponse()
		# response.delete_cookie('bookserviceLogin')
		auth.logout(request)
		return HttpResponseRedirect("/items/")
	except KeyError:
		pass
	return HttpResponseRedirect("/items/")

