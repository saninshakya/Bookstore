from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from review.forms import ReviewForm
from review.models import ReviewItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import sys
import datetime

def index(request, itemid):
	review = ReviewItem.objects.filter(deleted=False, item_id=itemid).order_by('id')
	context = {'review' : review}
	return render(request,'review/index.html', context)

@login_required()
def insert(request, itemid):
	try:
		form = ReviewForm()
		review = ReviewItem.objects.filter(deleted=False, item_id=itemid).order_by('id')
		if request.method == 'POST':
			form = ReviewForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				review = cd['review']
				created = datetime.datetime.now()
				modified = datetime.datetime.now()
				user = request.user.id
				result = ReviewItem.objects.create(review=review, item_id=itemid, createdBy_id=user, created=created, modified=created, deleted=False)
				if result:
					messages.add_message(request, messages.INFO, "Thank you for Review")
				else:
					messages.add_message(request, messages.ERROR, "Error occured. Please Try Again.")
				return HttpResponseRedirect('/review/' + itemid + '/')
			else:
				return render(request,'review/add.html', {'form':form, 'review':review})
		else:
			return render(request,'review/add.html', {'form':form, 'review':review})
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		return render(request,'review/index.html')