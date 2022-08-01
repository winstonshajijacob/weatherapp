# WeatherApp

WeatherApp is a Python web app for showing all cities with a particular weather condition

## Installation

Use pip to install requirements

```bash
pip install -r requirements.txt
```

## Usage

1. Navigate to the 'weather_env' folder
2. start the app by running the command
```python
python manage.py runserver
```
3. Open your browser and go to http://localhost:8000/
4. Use to Authenticate button to sign into an account that has access to the US cities spreadsheet. You will be redirected back to the main page after authentication.
5. Click on any weather condition to see all cities with that weather. (Note:This takes some time)

## Things that break the system

There are some city names in the format “city_name-county_name” that the API doesn't return a value for unless requested for separately

If the user who logs in does not have access to the Google Sheet with the city data the system doesn't work

If accessing the website via IP address instead of localhost:8000 it breaks the google auth


## Bugs/Improvements

Google oauth doesn't show a message on authentication

Caching fetched spreadsheet values so that we don't have to make repeated Google API calls

Caching fetched weather data so that we don't have to make repeated Openweather API calls.

While loading the spreadsheet values and doing all the API calls there is no indication of that process occuring.

