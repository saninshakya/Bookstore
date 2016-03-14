from django.db import models
from django.contrib.auth.models import User
from items.models import ItemList

class ChallengeOthers(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	item = models.ForeignKey(ItemList)
	challengedBy = models.ForeignKey(User, related_name='challengedBy')
	challengedTo = models.ForeignKey(User, related_name='challengedTo')
	acceptChallenge = models.BooleanField(default=False)
	challengeCompleted = models.BooleanField(default=False)
	challengedDate = models.DateField()
	challengeCompletedDate = models.DateField(blank=True, null=True)
	dueDate = models.DateField(blank=True, null=True)
	note = models.CharField(max_length=500, blank=True, null=True)
	deleted = models.BooleanField(default=False)
	class Meta:
		db_table = 'challenge_others'
