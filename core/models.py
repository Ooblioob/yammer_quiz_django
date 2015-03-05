from django.db import models

# Create your models here.
class question_text(models.Model):
	question_text = models.CharField(max_length=100)