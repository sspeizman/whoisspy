from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name

class Phrase(models.Model):
	name = models.CharField(max_length=200)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Group(models.Model):
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name

class UserProfile(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	is_spy = models.BooleanField(default=False)
	group = models.ManyToManyField(Group, blank=True)
	score = models.IntegerField(default=0)
	is_active = models.BooleanField(default=False)
	is_dead = models.BooleanField(default=False)
	phrase = models.ForeignKey(Phrase, blank=True, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.user.first_name

	def get_status_color(self):
		if self.is_dead:
			if self.is_spy:
				return 'red'
			else:
				return 'grey'
		else:
			return 'green'



