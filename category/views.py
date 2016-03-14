from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from category.models import CategoryList
from django.contrib import messages
import sys
from category.forms import CategoryForm
from django.contrib.auth.decorators import user_passes_test

def index(request):
	category_list = CategoryList.objects.filter(deleted=False).order_by('id')
	context = {'category_list' : category_list}
	return render(request,'category/index.html', context)

@user_passes_test(lambda u:u.is_staff)
def insert(request):
	try:
		args={}
		form = CategoryForm()
		if request.method == 'POST':
			form = CategoryForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				title = cd['title']
				result = CategoryList.objects.create(category=title, deleted=False)
				if result:
					messages.add_message(request, messages.INFO, "Category Added Successfully!")
				else:
					messages.add_message(request, messages.ERROR, "Error occured during category insertion. Please Try Again.")
				return HttpResponseRedirect('/category/')
			else:
				args['form'] = form	
				return render(request, 'category/add.html', args)
		else:
			args['form'] = form	
			return render(request, 'category/add.html', args)
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		form = CategoryForm()	
		return render(request, 'category/add.html', {'form':form})

@user_passes_test(lambda u:u.is_staff)
def edit(request, categoryid):
	try:
		# args={}
		category = get_object_or_404(CategoryList, pk=categoryid)
		form = CategoryForm(initial={'title': category.category})
		if request.method == 'POST':
			form = CategoryForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				title = cd['title']			
				result = CategoryList.objects.filter(id=categoryid).update(category=title)
				if result:
					messages.add_message(request, messages.INFO, "Category Updated Successfully!")
				else:
					messages.add_message(request, messages.ERROR, "Error occured during deleting category. Please Try Again.")
				return HttpResponseRedirect('/category/')
			else:
				# args['form'] = form	
				return render(request, 'category/edit.html', {'form':form, 'categoryid':categoryid})
		else:
			# args['form'] = form	
			return render(request, 'category/edit.html', {'form':form, 'categoryid':categoryid})
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		return render(request, 'category/index.html')

@user_passes_test(lambda u:u.is_staff)
def delete(request, categoryid):
	try:
		result = CategoryList.objects.filter(id=categoryid).update(deleted=True)
		if result:
			messages.add_message(request, messages.INFO, "Category Deleted Successfully!")
		else:
			messages.add_message(request, messages.INFO, "Error Occured.Try Again!")
		return HttpResponseRedirect('/category/')
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		return render(request, 'category/index.html')