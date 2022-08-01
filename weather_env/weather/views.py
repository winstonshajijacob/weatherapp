from django.shortcuts import render
from django.shortcuts import redirect
import requests
import pandas as pd
import google_auth_oauthlib.flow
from googleapiclient.discovery import build


mycreds = None

#Reads the spreadsheet data
def pull_sheet_data(CREDS,SPREADSHEET_ID,DATA_TO_PULL):
    creds = CREDS
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=DATA_TO_PULL).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=DATA_TO_PULL).execute()
        data1 = rows.get('values')
        #Can store the spreadsheet data to avoid repeated calls,I didn't do so here to as the spreadsheet values can change, therefore we'd need the updated list of cities
        print("COMPLETE: Data copied")
        return data1

#Loads the main page with a New York's weather as default
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},us&units=imperial&appid=4265d0817d44745731d9258ee83fe848'
    city = 'New York'
    weather_city = []
    city_weather = requests.get(url.format(city)).json() #Request the API data and convert the JSON to Python data types
    #Creating a dictionary with the information needed
    weather = {
        'city' : city,
        'temperature' : city_weather['main']['temp'],
        'wind' : int(city_weather['wind']['speed']),
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }
    weather_city.append(weather)
    
    context = {'weather_city' : weather_city}

    return render(request, 'weather/index.html', context) #returns the index.html template

#Initiates Google OAuth
def sheetSync(request):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes = SCOPES)
    flow.redirect_uri = 'http://localhost:8000/weather/oauth2callback'
    authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='false')
    request.session['state'] = state
    return redirect(authorization_url) #Google Oauth page

#Oauth callback which gives us the credentials we need to access the spreadsheet data
def oauth2callback(request):    
    state = request.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'],
    state=state)
    flow.redirect_uri = 'http://localhost:8000/weather/oauth2callback' 
    temp_var = request.build_absolute_uri()
    if "http:" in temp_var:
        temp_var = "https:" + temp_var[5:]
    authorization_response = temp_var
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    global mycreds
    mycreds = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}
    return redirect('http://localhost:8000/')

#Calls the weather api with spreadsheet data, uses Pandas to organize everything into an appropriate format and sends a dictionary to the front end.
def sheetPandas(wcond):
    global mycreds
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '1_Rxr-2jkJgWmmO6xLJJ61SHEXeRCUVIgv6cXXnvz438'
    DATA_TO_PULL = 'Cities'
    data = pull_sheet_data(mycreds,SPREADSHEET_ID,DATA_TO_PULL)
    df = pd.DataFrame(data[1:], columns=data[0])
    city_data = [] #dict to store weather info of all cities
    weather_city = [] #dict to store weather of cities with specified weather condition
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},us&units=imperial&appid=4265d0817d44745731d9258ee83fe848'
    for index, row in df.iterrows():
        city = row['City']
        city_weather = requests.get(url.format(city)).json() 
        if city_weather['cod'] !=200: #checks if city not found
            continue
        #Can add another if statement to check weather condition here 
        weather = {
        'city' : city,
        'state': row['State'],
        'temperature' : city_weather['main']['temp'],
        'wind' : int(city_weather['wind']['speed']),
        'description' : city_weather['weather'][0]['main'],
        'icon' : city_weather['weather'][0]['icon']
        }
        city_data.append(weather)
    #Used a seperate loop to filter as code can be modified to store above data and use below code to filter as needed,reducing API calls made
    for row in city_data:
        if row['description'] == wcond:
            weather_city.append(row)
    context = {'weather_city' : weather_city}
    return (context)
