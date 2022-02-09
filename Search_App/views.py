from itertools import count
from django.shortcuts import render
from .models import Search_History
from django.contrib.auth.models import User
from collections import Counter

# Create your views here.

def home(request):

     if request.method == 'POST':
          keyword = request.POST.get('keyword')
          user = request.user
          browser = request.META['HTTP_USER_AGENT']

          new_ob = Search_History()
          new_ob.user = user
          new_ob.keyword = keyword
          new_ob.browser = browser
          new_ob.save() 

     all_users = User.objects.all()

     all_keywords = Search_History.objects.all()
     all_dist_keywords = Search_History.objects.values('keyword').distinct()

     keyword_count = []
     for dist_key in all_dist_keywords:
          count = 0
          for key in all_keywords:
               if dist_key['keyword'] == key.keyword:
                    count+=1

          value = str(dist_key['keyword']+' (') + str(count)+' times found)'
          keyword_count.append(value)
         
     return render(request,'Search_App/home.html', context={'all_users':all_users,'all_keywords':keyword_count,})