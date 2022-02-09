from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Search_History(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_search')
     keyword = models.CharField(max_length=200)
     browser = models.CharField(max_length=100)
     #results = models.ManyToManyField(#)
     time = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.keyword
