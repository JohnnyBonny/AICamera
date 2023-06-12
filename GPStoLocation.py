import requests

# get the GPS latitude and longitude


# 33.78400047017209, -118.11419790073333 CSULB
37.80897793726442, -122.4122598135595
latitude = 33.838614
longitude =  -118.376501

# API used to convert the GPS coordinates to a human-readable location
Positionstack_API_Key = ""
Positionstack_URL = f"http://api.positionstack.com/v1/reverse?access_key={Positionstack_API_Key}&query={latitude},{longitude}&fields=results.label"

response = requests.get(Positionstack_URL)
location_name = response.json()["data"][0]["label"]

# API used to get the weather of the location
Weatherstack_API_Key = ""

Weatherstack_URL = f"http://api.weatherstack.com/current?access_key={Weatherstack_API_Key}&query={location_name}&units=f"
response = requests.get(Weatherstack_URL)
location_weather_description = response.json()["current"]["weather_descriptions"][0]
location_temperature = response.json()["current"]["temperature"]

del response

#return location_name,location_weather_description,locations_temperature