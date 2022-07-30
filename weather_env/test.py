import pandas as pd
import requests
df = pd.read_pickle('data.pkl')
# print(df)
city_data = []
url = 'http://api.openweathermap.org/data/2.5/weather?q={},us&units=imperial&appid=4265d0817d44745731d9258ee83fe848'
for index, row in df.iterrows():
    # print(row['City'],row['State'])
    city = row['City']

    city_weather = requests.get(url.format(city)).json() 
    if city_weather['cod'] !=200:
        continue
    weather = {
        'city' : city,
        'state': row['State'],
        'temperature' : city_weather['main']['temp'],
        'wind' : int(city_weather['wind']['speed']),
        'description' : city_weather['weather'][0]['main'],
        'icon' : city_weather['weather'][0]['icon']
    }
    # print(weather)
    city_data.append(weather)
for row in city_data:
        condition = 'Clouds'#drop down value
        if row['description'] == condition:
            print(row)