from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from category.models import CategoryList
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    try:
    	os.remove(os.path.join('static/images', filename))
    except OSError:
    	pass
    return os.path.join('static/images', filename)

def get_tableofContentfile_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    try:
    	os.remove(os.path.join('static/data/tableofcontent', filename))
    except OSError:
    	pass
    return os.path.join('static/data/tableofcontent', filename)

def get_abstractfile_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    try:
    	os.remove(os.path.join('static/data/abstract', filename))
    except OSError:
    	pass
    return os.path.join('static/data/abstract', filename)


def get_bulkfile_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    try:
    	os.remove(os.path.join('static/data', filename))
    except OSError:
    	pass
    return os.path.join('static/data', filename)

class ItemList(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	title = models.CharField(max_length=500)
	author = models.CharField(max_length=250)
	publisher = models.CharField(max_length=500)
	publicationDate = models.CharField(max_length=50)
	isbn = models.CharField(max_length=200)
	editionLanguage = models.CharField(max_length=50)
	awards = models.CharField(max_length=500)
	summary = models.TextField()
	coverImageUrl = models.CharField(max_length=500)
	url = models.CharField(max_length=500)
	category = models.ForeignKey(CategoryList)
	createdBy = models.ForeignKey(User)
	created = models.DateTimeField()
	modified = models.DateTimeField()
	deleted = models.BooleanField(default=False)
	class Meta:
		db_table = 'item_list'

class UploadFile(models.Model):
	file = models.ImageField(upload_to=get_file_path)
	created = models.DateTimeField()
	modified = models.DateTimeField()
	deleted = models.BooleanField(default=False)
	item = models.ForeignKey(ItemList)
	class Meta:
		db_table = 'item_cover_image'

class UploadItemBulk(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	file = models.FileField(upload_to=get_bulkfile_path, blank=True, null=True)
	uploadedDate = models.DateTimeField()
	uploadedBy = models.ForeignKey(User)
	class Meta:
		db_table = 'item_bulk_insertion'

class UploadTableofContent(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	file = models.FileField(upload_to=get_tableofContentfile_path, blank=True, null=True)
	uploadedDate = models.DateTimeField()
	modified = models.DateTimeField()
	deleted = models.BooleanField(default=False)
	item = models.ForeignKey(ItemList)
	class Meta:
		db_table = 'item_table_of_content'

		
class UploadAbstract(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	file = models.FileField(upload_to=get_abstractfile_path, blank=True, null=True)
	uploadedDate = models.DateTimeField()
	modified = models.DateTimeField()
	deleted = models.BooleanField(default=False)
	item = models.ForeignKey(ItemList)
	class Meta:
		db_table = 'item_abstract'