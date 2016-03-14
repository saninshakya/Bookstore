from django.db import models
import datetime
from django.contrib.auth.models import User
from items.models import ItemList

class ReviewItem(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	review = models.CharField(max_length=1000)
	item = models.ForeignKey(ItemList)
	createdBy = models.ForeignKey(User)
	created = models.DateTimeField()
	modified = models.DateTimeField()
	deleted = models.BooleanField(default=False)
	class Meta:
		db_table = 'review_item'

