from django.shortcuts import render
from django.shortcuts import redirect
import requests


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
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},us&units=imperial&appid=4265d0817d44745731d9258ee83fe848'

    city = 'Seattle'

    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

    # print(city_weather) #temporarily view output

    weather = {
        'city' : city,
        'temperature' : city_weather['main']['temp'],
        'wind' : int(city_weather['wind']['speed']),
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }

    context = {'weather' : weather}

    return render(request, 'weather/index.html', context) #returns the index.html template

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
    return redirect(authorization_url) #google oauth popup


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
    print("before")
    flow.fetch_token(authorization_response=authorization_response)
    print("after")

    
    credentials = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '1_Rxr-2jkJgWmmO6xLJJ61SHEXeRCUVIgv6cXXnvz438'
    DATA_TO_PULL = 'Cities'
    data = pull_sheet_data(credentials,SPREADSHEET_ID,DATA_TO_PULL)
    df = pd.DataFrame(data[1:], columns=data[0])
    print(df)
    # credentials = None
    return render(request, 'weather/index.html')