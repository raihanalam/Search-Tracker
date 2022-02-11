from operator import mod
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Search_History(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_search',blank=True)
     keyword = models.CharField(max_length=200)
     ip = models.CharField(max_length=100,blank=True)
     browser = models.CharField(max_length=100,blank=True)
     #results = models.ManyToManyField(#)
     time = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.keyword
