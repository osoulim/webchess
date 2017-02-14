from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Game(models.Model):
	state = models.CharField(max_length=100, default="rnbqkbnr/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBNR//")
	player = models.OneToOneField(User)
	
	def reset_game(self):
		self.state = "rnbqkbnr/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBNR//"