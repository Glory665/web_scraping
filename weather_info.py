import requests
import json
import os
from dotenv import load_dotenv

load_dotenv("./.env")


appid = os.getenv("appid", 0)
city = input("Enter your city: ")


def get_coord(city):
    res = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={appid}"
    )
    if not res.json():
        return None
    coordinates = (res.json()[0]["lat"], res.json()[0]["lon"])
    return coordinates


def get_weather(city):
    coordinates = get_coord(city)
    if not coordinates:
        return None
    lat, lon = coordinates[0], coordinates[1]
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"units=metric&lat={lat}&lon={lon}&appid={appid}"
    )
    print(f"В городе {city} {res.json()['main']['temp']} градусов по Кельвину")


def main():
    get_weather(city)


if __name__ == "__main__":
    main()