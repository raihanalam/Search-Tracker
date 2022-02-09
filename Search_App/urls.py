from . import views
from django.urls import path

app_name = 'Search_App'

urlpatterns = [
    path('', views.home, name='home' ),
]
