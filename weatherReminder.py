import schedule
import time
import requests
from twilio.rest import Client

from secrets import account_sid, auth_token, from_phone_number, to_phone_number
from getWeatherInfo import latitude, longitude, base_url


def get_weather(latitude, longitude):
    response = requests.get(base_url)
    data = response.json()
    return data

def celcius_to_fahrenheit(celcius):
    return (celcius * 9/5) + 32

def send_text_message(body):

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body = body, 
        from_ = from_phone_number,
        to = to_phone_number
    )
    print ("Text message sent!")

def send_weather_update():
    weather_data = get_weather(latitude, longitude)
    temperature_celcius = weather_data["hourly"]["temperature_2m"][0]
    relativehumidity = weather_data["hourly"]["relativehumidity_2m"][0]
    wind_speed = weather_data["hourly"]["windspeed_10m"][0]
    temperature_fahrenheit = celcius_to_fahrenheit(temperature_celcius)

    weather_info = (
        f"Good morning! \n"
        f"Current weather in City, State: \n"
        f"Temperature: {temperature_fahrenheit:.2f} F\n"
        f"Relative humidity: {relativehumidity}% \n"
        f"Wind Speed: {wind_speed} m/s\n"
    )

    send_text_message(weather_info)


def main():
    schedule.every().day.at("07:40").do(send_weather_update)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

