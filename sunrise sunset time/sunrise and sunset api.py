import requests
from datetime import datetime

my_latitude = 28.7041  # location data from internet (this is DMS 20° 35' 37.32"), convert DMS into degree
my_longitude = 77.1025

parameters = {
    "lat": my_latitude,
    "lng": my_longitude,
    "formatted": 0,  # parameter of api to convert time into 24 hours format
}

# note: sunrise is in UTC time mode so UTC 12:30 AM (or 00:30 AM) means IST 6 AM.
# note  sunset time in utc is 12:30 PM means ist 6 PM. (IST = UTC + 5:30)

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
# print(data)

sunrise = data["results"]["sunrise"]
sunset = data["results"]["sunset"]
# print(f"sunrise: {sunrise}")  # e.g. 00:34:43+00:00 (converted into 24 hour by formatted:0)
# print(f"sunset: {sunset}")   # e.g. 12:31:17+00:00

sunrise_time = int(sunrise.split("T")[1].split(":")[0]) + 6
sunset_time = int(sunset.split("T")[1].split(":")[0]) + 6
# 6 add because IST = UTC + 5:30
print(f"sunrise time: {sunrise_time}")
print(f"sunset time: {sunset_time}")

# time_now = datetime.now()
# utc_time = datetime.utcnow()
# print(f"current UTC time: {utc_time} and IST time: {time_now}")




