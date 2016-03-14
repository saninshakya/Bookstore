from django.db import models
from django.contrib.auth.models import User
from items.models import ItemList

class WishList(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	user = models.ForeignKey(User)
	item = models.ForeignKey(ItemList)
	status = models.CharField(max_length=50, blank=True, null=True)
	dateAdded = models.DateTimeField()
	readDate = models.DateField(blank=True, null=True)   #blank = true is validation related but null = true is completely database related
	deleted = models.BooleanField(default=False)
	class Meta:
		db_table = 'wish_list'