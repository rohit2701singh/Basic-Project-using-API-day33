import requests
from datetime import datetime
import smtplib
import time
import os

MY_LAT = 28.7041
MY_LONG = 77.1025

MY_MAIL = os.environ.get("EMIL_ID")
MY_PASSWD = os.environ.get("PASSWORD")

# note1: If the ISS is close to my current position, and it is currently dark, then send email to tell me to look up.
# note2: run the code every 60 seconds.


def iss_location_check(my_latitude, my_longitude,):
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(f"current ISS latitude: {iss_latitude} and longitude: {iss_longitude}")

    # iss_latitude = 30  # for testing purpose
    # iss_longitude = 80
    # iss location can be anywhere between my_lat-5 and my_lat+5 i.e. 15 < iss position < 25
    if (my_latitude - 5 < iss_latitude < my_latitude + 5) and (my_longitude - 5 < iss_longitude < my_longitude + 5):
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(f"your sunrise time: {sunrise} and sunset time: {sunset}")

    utc_time_now = datetime.utcnow().hour
    print(utc_time_now)

    if sunset <= utc_time_now or utc_time_now <= sunrise:   # check nighttime
        return True
    else:
        return False


iss_overhead = iss_location_check(MY_LAT, MY_LONG,)

while True:
    time.sleep(60)  # run while loop after every 60 seconds.
    if iss_overhead and is_night():
        print("ISS is near and its night time.")
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_MAIL, password=MY_PASSWD)
            connection.sendmail(
                from_addr=MY_MAIL,
                to_addrs=MY_MAIL,
                msg="subject: ISS overhead Look up\n\nInternational Space Station is near you. Look up"
            )
        print("email sent successfully.")
    else:
        print("ISS is far away. Can't send email.")
