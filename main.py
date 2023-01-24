import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 47.606209
MY_LONG = -122.332069
TEST_EMAIL = "test@hotmail.com"
TEST_PASSWORD = "test"


def is_iss_overhead(iss_location):
    (iss_lat, iss_long) = iss_location
    lat_close = MY_LAT - 5 <= iss_lat <= MY_LAT + 5
    long_close = MY_LONG - 5 <= iss_long <= MY_LONG + 5
    return lat_close & long_close


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    sun_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    sun_data = sun_response.json()
    sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    return sunset <= time_now <= sunrise


iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()
iss_data = iss_response.json()
longitude = float(iss_data["iss_position"]["longitude"])
latitude = float(iss_data["iss_position"]["latitude"])
iss_position = (latitude, longitude)


# if it's dark and the ISS is close to my current location, send me an email
# check this condition every 60 seconds
while True:
    time.sleep(60)
    if is_dark() and is_iss_overhead(iss_position):
        with smtplib.SMTP("smtp.office365.com") as connection:
            connection.starttls()
            connection.login(TEST_EMAIL, TEST_PASSWORD)
            connection.sendmail(
                from_addr=TEST_EMAIL,
                to_addrs=TEST_EMAIL,
                msg="Subject:Look Up! \n\nThe ISS is above you in the sky"
            )