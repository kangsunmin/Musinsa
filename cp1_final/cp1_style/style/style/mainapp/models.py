from django.db import models

class information_user(models.Model):
    gender = models.CharField(max_length=200)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    large_category = models.CharField(max_length=200)
    medium_category = models.CharField(max_length=200)

class review_user(models.Model): 
    gender = models.CharField(max_length=200)
    recommend = models.CharField(max_length=200)
    what = models.CharField(max_length=200)