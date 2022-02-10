from django.shortcuts import render
from .models import Search_History
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.core import serializers
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
     all_single_keys = []
     for dist_key in all_dist_keywords:
          count = 0
          for key in all_keywords:
               if dist_key['keyword'] == key.keyword:
                    count+=1

          value = str(dist_key['keyword']+' (') + str(count)+' times found)'
          keyword_count.append(value)
          all_single_keys.append({
               'key': dist_key['keyword'],
               'count': count
          })
         
     return render(request,'Search_App/home.html', context={'all_users':all_users,'all_keywords':all_single_keys,})


def filter(request):
     keyword = request.GET.get('keyword')
     users = request.GET.get('users')
     key_list = keyword.split(',')

     user_list = users.split(',')

     myUser = User.objects.filter(username__in = user_list)
     #print(key_list)

     # Any process that you want

     search_objects = Search_History.objects.filter(user__in = myUser) and Search_History.objects.filter(keyword__in = key_list)
     #search_ob = list(search_objects)
     #search_ob = json.dumps(search_objects)
     filter_result = serializers.serialize('json', search_objects)
     search_new = json.loads(filter_result)
    

     
    
     print(search_new)
     data = {
          'all_search_data': search_new
     }
     return JsonResponse(data)