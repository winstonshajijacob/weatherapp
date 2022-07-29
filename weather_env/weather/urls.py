from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),  #the path for our index view
    path('sheetSync', views.sheetSync, name='sheet_sync'),
    path('weather/oauth2callback',views.oauth2callback, name = "oauth2callback"),
    
]