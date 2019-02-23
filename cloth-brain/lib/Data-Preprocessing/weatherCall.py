# Import libraries
import config
import requests
import json
import time

# Set api key
api_key = config.api_key

# Checks if each key exists in a given entry
def keys_check(c, cw):
    key_missing = False
    if ('id' not in c): key_missing = True
    if ('name' not in c): key_missing = True
    if ('country' not in c): key_missing = True
    
    if ('main' not in cw): key_missing = True
    else :
        if ('temp' not in cw): key_missing = True
        if ('pressure' not in cw): key_missing = True
        if ('humidity' not in cw): key_missing = True
    
    if ('wind' not in cw): key_missing = True
    else :
        if ('speed' not in cw): key_missing = True

    return not key_missing

# Read JSON file
with open('city.list.json', encoding='utf8') as city_json:
    city_data = json.load(city_json)

# Initialize JSON object array
output_weather = []

# Open the empty JSON file and append entries from API calls
with open('city_weather.json', mode='a', encoding='utf8') as city_weather_json:
    # Loops through entries and accesses the city id
    for i, city in enumerate(city_data):
        city_id = str(city['id'])       
        url = "https://api.openweathermap.org/data/2.5/weather?id="+city_id+"&appid="+api_key+"&units=imperial"
        city_weather = requests.get(url).json()

        keys_exist = keys_check(city, city_weather)
        if (keys_exist):
            entry = {
                'id': city_id,
                'name': city['name'],
                'country': city['country'],
                'temp': city_weather['main']['temp'],
                'wind_speed': city_weather['wind']['speed'],
                'pressure': city_weather['main']['pressure'],
                'humidity': city_weather['main']['humidity'],
                'description': city_weather['weather'][0]['description']
            }

            output_weather.append(entry)

        # Pause every 50 calls, up to 1000 entries
        if (i > 0 and i % 50 == 0):
            if (i == 1000):
                print('done')
                break
            time.sleep(60)
    
    # Dump ouput array to empty JSON file
    json.dump(output_weather, city_weather_json, indent=4)