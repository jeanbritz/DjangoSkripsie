import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Poll(models.Model):
	
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField('data published')
	
	def __unicode__(self):
		return unicode(self.question)
	
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date < now
	
class Choice(models.Model):
	
	poll = models.ForeignKey(Poll)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	
	def __unicode__(self):
		return unicode(self.choice_text) + "Votes: " + unicode(self.votes)
	
