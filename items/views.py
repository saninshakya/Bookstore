from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from category.models import CategoryList
from items.models import ItemList, UploadFile, UploadItemBulk, UploadTableofContent, UploadAbstract
from items.forms import ItemForm, SelectXMLForm
import sys
import os
import urllib.request
import shutil
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import xml.etree.ElementTree as etree
import textwrap
from django.conf import settings


def index(request):
	item_list = ItemList.objects.filter(deleted=False).order_by('id')
	return render(request,'items/index.html', {'item_list' : item_list})

@user_passes_test(lambda u:u.is_staff)
def insert(request):
	try:
		args={}
		form = ItemForm()
		if request.method == 'POST':
			form = ItemForm(request.POST, request.FILES)
			if form.is_valid():
				cd = form.cleaned_data
				title = cd['title']
				author = cd['author']
				pub = cd['pub']
				pub_date = cd['pub_date']
				isbn = cd['isbn']
				lang = cd['lang']
				url = cd['url']
				awards = cd['awards']
				summary = cd['summary']
				category = cd['category']
				img_url =  cd['img_url'] 
				created = datetime.datetime.now()
				user = request.user.id
				result = ItemList.objects.create(title=title, author=author, publisher=pub, publicationDate=pub_date, isbn=isbn, editionLanguage=lang, awards=awards, summary=summary, coverImageUrl=img_url, url=url, category_id=category, createdBy_id=user, created=created, modified=created, deleted=False)
				if result:
					# For uploading local cover image
					if cd['local_img']:
						local_img  = UploadFile(file = cd['local_img'], created=created, modified=created, item_id=result.id)
						local_img.save()
					# For uploading table of content file
					if cd['table_of_content']:
						table_of_content = UploadTableofContent(file = cd['table_of_content'], uploadedDate=created, modified=created, item_id=result.id)
						table_of_content.save()
					# For uploading abstract file
					if cd['abstract']:
						abstract = UploadAbstract(file = cd['abstract'], uploadedDate=created, modified=created, item_id=result.id)
						abstract.save()
					# For copying image from url
					if img_url:
						filename = img_url.split('/')[-1] # Gets filename from URL
						urllib.request.urlretrieve( img_url, filename ) # This copies the file in project folder eg: inside F:/Bookservice
						# For moving the file from project folder to static/images/URLImages
						oldpath = settings.BASE_DIR + "/" + filename
						newpath = settings.BASE_DIR + '/static/images/URLImages/'
						shutil.move(oldpath,newpath)
					messages.add_message(request, messages.INFO, "Item Added Successfully!")
				else:
					messages.add_message(request, messages.ERROR, "Error occured during item insertion. Please Try Again.")
				return HttpResponseRedirect('/items/')
			else:
				args['form'] = form	
				return render(request, 'items/add.html', args)
		else:
			args['form'] = form	
			return render(request, 'items/add.html', args)
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		return render(request, 'items/index.html')

def detail(request, itemid):
	item = get_object_or_404(ItemList, pk=itemid, deleted=False)
	if item.coverImageUrl:
		imageurl = item.coverImageUrl
		filename = imageurl.split('/')[-1]
	# book_image = get_object_or_404(UploadFile, item_id=itemid, deleted=False)
	# # return render(request, 'items/detail.html', {'item': item, 'image':book_image.file, 'imageurl':filename})
	# if book_image:
	# 	return render(request, 'items/detail.html', {'item': item, 'filenameFromUrl':filename, 'image':book_image.file})
	# else:
		return render(request, 'items/detail.html', {'item': item, 'filenameFromUrl':filename})
	else:
		return render(request, 'items/detail.html', {'item': item})


@user_passes_test(lambda u:u.is_staff)
def edit(request, itemid):
	try:
		# args={}
		#select the item to be edited
		item = get_object_or_404(ItemList, pk=itemid)
		# get filename of image from url (cover image from url)
		oldimageurl = item.coverImageUrl
		oldfilename=''
		if oldimageurl:
			oldfilename = oldimageurl.split('/')[-1] # path and filename is stored. So it is split to get filename only. if empty coverimageurl then oldfilename is passed empty
		form = ItemForm(initial={'title': item.title, 'author':item.author, 'pub':item.publisher, 'pub_date':item.publicationDate,'isbn':item.isbn, 'lang':item.editionLanguage,'awards':item.awards,'summary':item.summary, 'url':item.url, 'category':item.category_id, 'img_url':item.coverImageUrl})
		if request.method == 'POST':
			form = ItemForm(request.POST, request.FILES)
			if form.is_valid():
				cd = form.cleaned_data
				title = cd['title']
				author = cd['author']
				pub = cd['pub']
				pub_date = cd['pub_date']
				isbn = cd['isbn']
				lang = cd['lang']
				url = cd['url']
				awards = cd['awards']
				summary = cd['summary']
				category = cd['category']
				local_img = cd['local_img']
				img_url =  cd['img_url'] 
				table_of_content = cd ['table_of_content']
				abstract = cd['abstract']
				modified = datetime.datetime.now()
				result = ItemList.objects.filter(id=itemid).update(title=title, author=author, publisher=pub, publicationDate=pub_date, isbn=isbn, editionLanguage=lang, awards=awards, summary=summary, url=url, coverImageUrl=img_url, category_id=category,  modified=modified)
				if result:
					if local_img:
						# book_image = UploadFile.objects.filter(item_id=itemid, deleted=False)
						# del_img = book_image.file
						# os.remove(del_img)		
						# book_image.delete()			
						result = UploadFile.objects.filter(item_id=itemid).update(deleted=True, modified=modified)
						local_img  = UploadFile(file = request.FILES['local_img'], created=modified, modified=modified, item_id=itemid)
						local_img.save() 
					# For editing image from url. The old image from url is also deleted form folder
					if img_url != oldimageurl: 
						if oldimageurl:
							# Removes old file if url is changed
							oldimagepath = settings.BASE_DIR + '/static/images/URLImages/' + oldfilename
							os.remove(oldimagepath)
						if img_url:
							# copies new file if url is changed
							filename = img_url.split('/')[-1] # Gets filename from URL
							urllib.request.urlretrieve( img_url, filename ) # This copies the file in project folder eg: inside F:/Bookservice
							# For moving the file from project folder to static/images/URLImages
							oldpath = settings.BASE_DIR + "/" + filename
							newpath = settings.BASE_DIR + '/static/images/URLImages/'
							shutil.move(oldpath,newpath)
					# if user selects new table of content pdf file
					if table_of_content:
						#set deleted = true to old record
						result = UploadTableofContent.objects.filter(item_id=itemid).update(deleted=True, modified=modified)
						table_of_content = UploadTableofContent(file = cd['table_of_content'], uploadedDate=modified, modified=modified, item_id=itemid)
						table_of_content.save()
					# if user selects new abstract pdf file
					if abstract:
						#set deleted = true to old record
						result = UploadAbstract.objects.filter(item_id=itemid).update(deleted=True, modified=modified)
						abstract = UploadAbstract(file = cd['abstract'], uploadedDate=modified, modified=modified, item_id=itemid)
						abstract.save()
					messages.add_message(request, messages.INFO, "Item Edited Successfully!")
				else:
					messages.add_message(request, messages.ERROR, "Error occured. Please Try Again.")
				return HttpResponseRedirect('/items/')
			else:
				# args['form'] = form	
				return render(request, 'items/edit.html', {'form':form, 'itemid':itemid, 'imageurl':item.coverImageUrl})
		else:
			# args['form'] = form	
			#For selecting the uploaded local cover image and pass to templates
			localbook_image = UploadFile.objects.filter(item_id=itemid, deleted=False)
			if localbook_image:
				return render(request, 'items/edit.html', {'form':form, 'itemid':itemid, 'item':item, 'filename_from_url':oldfilename , 'image':localbook_image})
			else: # if local cover image not available no need to pass to template
				return render(request, 'items/edit.html', {'form':form, 'item':item, 'itemid':itemid, 'filename_from_url':oldfilename})
	except OSError:
		print ("No file for Delete ")
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		return render(request, 'items/index.html')

@user_passes_test(lambda u:u.is_staff)
def delete(request, itemid):
	try:
		result = ItemList.objects.filter(id=itemid).update(deleted=True)
		messages.add_message(request, messages.INFO, "Item Deleted Successfully!")
		return HttpResponseRedirect('/items/')
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		return render(request, 'items/index.html')

def fixtag(ns, tag, nsmap):
	return '{' + nsmap[ns] + '}' + tag

@user_passes_test(lambda u:u.is_staff)
def insert_bulk(request):
	# tree = ET.parse('static/data/sampledata.xml')
	# root = tree.getroot()
	# # return HttpResponse(root.tag) # displays metadata
	# xmlfiledata = []
	# for items in root:
	# 	# return HttpResponse(items.text)
	# 	xmlfiledata.append({'title': items.tag})
	# return render(request, 'items/bulkdisplay.html', {'items' : xmlfiledata})
	# create an XMLReader
	try:
		args={}
		form =  SelectXMLForm()
		if request.method == 'POST':
			form = SelectXMLForm(request.POST, request.FILES)
			# if form.is_valid():
			# cd = form.cleaned_data
			uploaded = datetime.datetime.now()
			user = request.user.id
			xmL = request.FILES['file']
			# update the database
			result = UploadItemBulk(file=xmL, uploadedDate=uploaded, uploadedBy_id=user)
			result.save()
			filepath = settings.BASE_DIR + "/" + str(result.file)
			nsmap = {}
			xmlfiledata = [] # list created
			dc ='{http://purl.org/dc/elements/1.1/}'
			for event, elem in etree.iterparse(filepath, events=('start', 'end', 'start-ns', 'end-ns')):
				if event == 'start-ns':
					ns, url = elem  #ns = xsi , url = http://www.w3.org/2001/XMLSchema-instance
					nsmap[ns] = url
				elif event == 'start' and elem.tag == 'description':
					childelement = True
				elif event == 'end' and childelement == True:
					# if elem.tag == fixtag('GAML', 'peptide', nsmap):
					# 	result = process_peptide(elem, nsmap)
					# 	results.append(result)
						
					if elem.tag == dc + 'title':
						xmlfiledata.append({'title': elem.text}) # append Adds an item to the end of the list.
					
					elif elem.tag == dc + 'author':
						xmlfiledata.append({'author': elem.text})
					
					elif elem.tag == dc + 'publisher':
						xmlfiledata.append({'publisher': elem.text})
					
					elif elem.tag == dc + 'publicationdate':
						xmlfiledata.append({'publicationdate': elem.text})

					elif elem.tag == dc + 'isbn':
						xmlfiledata.append({'isbn': elem.text})

					elif elem.tag == dc + 'language':
						xmlfiledata.append({'language': elem.text})

					elif elem.tag == dc + 'awards':
						xmlfiledata.append({'awards': elem.text})

					elif elem.tag == dc + 'summary':
						xmlfiledata.append({'summary': elem.text})

					elif elem.tag == dc + 'image':
						xmlfiledata.append({'image': elem.text})

					elif elem.tag == dc + 'coverimageurl':
						xmlfiledata.append({'coverimageurl': elem.text})

					elif elem.tag == dc + 'identifier':
						xmlfiledata.append({'identifier': elem.text})

					elif elem.tag == 'description':
						created = datetime.datetime.now()
						user = request.user.id
						title = textwrap.dedent(xmlfiledata[0]['title']).strip()
						author = textwrap.dedent(xmlfiledata[1]['author']).strip()
						publisher = textwrap.dedent(xmlfiledata[2]['publisher']).strip()
						publicationdate = textwrap.dedent(xmlfiledata[3]['publicationdate']).strip()
						isbn = textwrap.dedent(xmlfiledata[4]['isbn']).strip()
						language = textwrap.dedent(xmlfiledata[5]['language']).strip()
						awards = textwrap.dedent(xmlfiledata[6]['awards']).strip()
						summary = textwrap.dedent(xmlfiledata[7]['summary']).strip()
						image = textwrap.dedent(xmlfiledata[8]['image']).strip()
						coverimage = textwrap.dedent(xmlfiledata[9]['coverimageurl']).strip()
						url = textwrap.dedent(xmlfiledata[10]['identifier']).strip()
						# return HttpResponse(title + author + publisher + publicationdate + isbn + language + awards + summary + image + coverimage + url)
						result = ItemList.objects.create(title=title, author=author, publisher=publisher, publicationDate=publicationdate, isbn=isbn, editionLanguage=language, awards=awards, summary=summary, coverImageUrl=coverimage, url=url, category_id=2, createdBy_id=user, created=created, modified=created, deleted=False)
						if result:
							if coverimage:
								filename = coverimage.split('/')[-1] # Gets filename from URL
								urllib.request.urlretrieve( coverimage, filename ) # This copies the file in project folder eg: inside F:/Bookservice
								# For moving the file from project folder to static/images/URLImages
								oldpath = settings.BASE_DIR + "/" + filename
								newpath = settings.BASE_DIR + '/static/images/URLImages/'
								shutil.move(oldpath,newpath)
							messages.add_message(request, messages.INFO, "Items Added Successfully!")
						else:
							messages.add_message(request, messages.ERROR, "Error occured during items insertion. Please Try Again.")
						childelement = False
						elem.clear()
						xmlfiledata.clear()

					
		
			return render(request, 'items/bulkdisplay.html', {'items' : xmlfiledata, 'form':form})

			# else:
			# 	args['form'] = form	
			# 	return render(request,'items/bulkdisplay.html',args)	 	
			# return render(request, 'items/bulkdisplay.html', {'items' : xmlfiledata, 'form':form})
						# result = process_peptide(elem, nsmap)
						# results.append(result)
		else:
			args['form'] = form	
			return render(request,'items/bulkdisplay.html',args)
	except:
		messages.add_message(request, messages.ERROR, sys.exc_info()[1])
		return render(request, 'items/bulkdisplay.html',{ 'form':form })

def pdf_download(request, filename):
	return HttpResponse(filename)
	path = os.expanduser('~/files/pdf/')
	wrapper = FileWrapper(file(filename,'rb'))
	response = HttpResponse(wrapper, content_type=mimetypes.guess_type(filename)[0])
	response['Content-Length'] = os.path.getsize(filename)
	response['Content-Disposition'] = "attachment; filename=" + filename
	return response

