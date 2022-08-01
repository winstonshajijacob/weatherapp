from django.urls import path, include
from . import views
import weather.weather_conditions

urlpatterns = [
    path('', views.index),  #the path for our index view
    path('sheetSync', views.sheetSync, name='sheet_sync'),
    path('weather/oauth2callback',views.oauth2callback, name = "oauth2callback"),
    path('cloud', weather.weather_conditions.cloud, name='cloud'),
    path('thunderstorm', weather.weather_conditions.thunderstorm, name='thunderstorm'),
    path('drizzle', weather.weather_conditions.drizzle, name='drizzle'),
    path('rain', weather.weather_conditions.rain, name='rain'),
    path('snow', weather.weather_conditions.snow, name='snow'),
    path('atmosphere', weather.weather_conditions.atmosphere, name='atmosphere'),
    path('clear', weather.weather_conditions.clear, name='clear'),

]