from django.db import models

class CategoryList(models.Model):
	id = models.AutoField(primary_key=True)
	category =  models.TextField()
	deleted = models.BooleanField(default=False)
	class Meta:
		db_table = 'category_list'
