from django.shortcuts import render
from .models import Search_History
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.

def home(request):
     if request.method == 'POST':
          keyword = request.POST.get('keyword')
          user_ip = visitor_ip_address(request)
          browser = request.META['HTTP_USER_AGENT']

          new_ob = Search_History()
          try:
               user = request.user
               new_ob.user = user
          except:
               print('Unknown user')
          new_ob.keyword = keyword
          new_ob.ip = user_ip
          new_ob.browser = browser
          new_ob.save() 

     all_users = User.objects.all()

     all_keywords = Search_History.objects.all()
     all_dist_keywords = Search_History.objects.values('keyword').distinct()

     #Counting all single keyword
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

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
def filter(request):

     #Any process that you want
     #Getting all data from JS
     keyword = request.GET.get('keyword')
     users = request.GET.get('users')
     time_range = request.GET.get('times')

     try:
          #Splitting them to list
          key_list = keyword.split(',')
          user_list = users.split(',')
          time_list = time_range.split(',')

          #Checking the maximum time range
          max_time = 0
          for i in time_list:
               i = int(i)
               if i > max_time:
                    max_time = i
          
          #Decreasing the time based on time range
          #now_datetime = datetime.now()
          now_datetime = timezone.now()

          if max_time == 1:
               range_time = now_datetime - timedelta(hours=24)
          elif max_time == 7:
               range_time = now_datetime - timedelta(hours=24*7)
          elif max_time == 30:
               range_time = now_datetime - timedelta(hours=24*30)
          

          #print(datetime.date(range_time))

          #start_date = datetime.date(2005, 1, 1)
          #end_date = datetime.date(2005, 3, 31)
          

          start_date = datetime.date(range_time)
          end_date = datetime.date(now_datetime)
     except:
          print("Some value my not filled!")

     myUser = User.objects.filter(username__in = user_list)

     #print(start_date,end_date)
     #print(key_list)
     if keyword == '' and users == '' and time_range == '': 
          print('All fields are empty.')
     elif keyword != '' and users == '' and time_range == '':
          search_objects = Search_History.objects.filter(keyword__in = key_list,)
          filter_result = serializers.serialize('json', search_objects)
          search_new = json.loads(filter_result)

     elif keyword !='' and users != '' and time_range == '':

          search_objects = Search_History.objects.filter(user__in = myUser, keyword__in = key_list,)
          filter_result = serializers.serialize('json', search_objects)
          search_new = json.loads(filter_result)

     elif users != '' and keyword == '' and time_range == '':
          search_objects = Search_History.objects.filter(user__in = myUser)
          filter_result = serializers.serialize('json', search_objects)
          search_new = json.loads(filter_result)
     
     elif time_range != '' and users != '' and keyword == '' :
          search_objects = Search_History.objects.filter(user__in = myUser, time__range=(start_date, end_date))
          filter_result = serializers.serialize('json', search_objects)
          search_new = json.loads(filter_result)

     elif time_range != '' and users == '' and keyword == '' :
          search_objects = Search_History.objects.filter(time__range=(start_date, end_date))
          filter_result = serializers.serialize('json', search_objects)
          search_new = json.loads(filter_result)

     elif time_range != '' and users == '' and keyword != '' :
          search_objects = Search_History.objects.filter(keyword__in = key_list,time__range=(start_date, end_date))
          filter_result = serializers.serialize('json', search_objects)
          search_new = json.loads(filter_result)
          
     elif keyword  != '' and users != '' and time_range != '':
          search_objects = Search_History.objects.filter(user__in = myUser, keyword__in = key_list, time__range=(start_date, end_date)) #and Search_History.objects.filter(time__range=(start_date, end_date)) # and Search_History.objects.filter(keyword__in = key_list, time__range=(start_date, end_date) )
          #search_ob = list(search_objects)
          #search_ob = json.dumps(search_objects)
          filter_result = serializers.serialize('json', search_objects)
          search_new = json.loads(filter_result)
     else:
          search_objects = Search_History.objects.filter(user__in = myUser, keyword__in = key_list)
          filter_result = serializers.serialize('json', search_objects)
          search_new = json.loads(filter_result)

    
     #print(search_new)
     data = {
          'all_search_data': search_new
     }
     return JsonResponse(data)

