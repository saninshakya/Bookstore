from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from wishlist.models import WishList
import datetime
from django.contrib import messages
import sys
from django.contrib.auth.decorators import login_required

@login_required()
def index(request):
	wishlists = WishList.objects.filter(deleted=False, user_id=request.user.id).order_by('-id')
	return render(request, 'wishlist/index.html', {'wishlists' : wishlists})

@login_required()
def insert(request, itemid):
	try:
		user = request.user.id
		created = datetime.datetime.now()
		result = WishList.objects.create(user_id=user, item_id=itemid, dateAdded=created, deleted=False)
		if result:
			messages.add_message(request, messages.INFO, "Item Added to Your WishList!")
		else:
			messages.add_message(request, messages.ERROR, "Error occured. Please Try Again.")
		return HttpResponseRedirect('/items/')
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		return render(request, 'items/index.html')

@login_required()
def update(request, wishid):
	try:
		if request.method == 'POST':
			status = request.POST['status']
			readdate = request.POST['readdate']
			if readdate!="":
				result = WishList.objects.filter(id=wishid).update(status=status, readDate=readdate)
			else:
				result = WishList.objects.filter(id=wishid).update(status=status)
			if result:
				return HttpResponseRedirect('/wishlist/')
			else:
				return HttpResponse("error")
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		return render(request, 'wishlist/index.html')

@login_required()
def delete(request, wishid):
	try:
		result = WishList.objects.filter(id=wishid).update(deleted=True)
		if result:
			return HttpResponseRedirect('/wishlist/')
		else:
			return HttpResponse("error")
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		return render(request, 'wishlist/index.html')