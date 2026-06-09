import requests
from discord import SyncWebhook
import os



OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API")
WEBHOOK_KEY = os.environ.get("WEBHOOK")


webhook = SyncWebhook.from_url(WEBHOOK_KEY)

parameters = {
    "appid": api_key,
    "lat": 11.8764,
    "lon": 75.3738,
    "cnt": 5
}

response = requests.get(url=OWM_ENDPOINT, params=parameters)
response.raise_for_status()

weather_data = response.json()

will_rain = False

for hour_data in weather_data["list"]:
    if hour_data["weather"][0]["id"] < 700:
        will_rain = True
rain =( f"# 6AM {weather_data["list"][0]["weather"][0]["description"]}\n"
       f"# 9AM {weather_data["list"][1]["weather"][0]["description"]}\n"
       f"# 12AM {weather_data["list"][2]["weather"][0]["description"]}\n"
       f"# 3PM {weather_data["list"][3]["weather"][0]["description"]}\n"
        f"# 6PM {weather_data["list"][4]["weather"][0]["description"]}\n"
        )

if will_rain:
    webhook = SyncWebhook.from_url(WEBHOOK_KEY)
    webhook.send(f"**Grabbing an umbrella is definitely a smart move to stay dry today.\n# {rain} **")
