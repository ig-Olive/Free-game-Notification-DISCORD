import requests
from discord import SyncWebhook,Embed
import os



OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API")
WEBHOOK_KEY = os.environ.get("WEBHOOK")

### FREE GAME ###
STEAM = os.environ.get("STEAM")
EPICGAMES = os.environ.get("EPICGAMES")


### FREE GAME ###


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

### FREE GAME ALERT ###

params = {
    "platform": "steam",
    "type": "game"
}

response_steam = requests.get(url="https://www.gamerpower.com/api/giveaways", params=params)
giveaways_steam = response_steam.json()

### Steam Free games loop ###

for i in range(len(giveaways_steam)):

    embed = Embed(
        title=giveaways_steam[i]["title"],
        description=f"{giveaways_steam[i]['worth']}\n{giveaways_steam[0]["end_date"].split()[0]}\n{giveaways_steam[0]["open_giveaway_url"]}",
    )
    embed.set_image(url=giveaways_steam[i]["image"])


    webhook_steam = SyncWebhook.from_url(STEAM)
    webhook_steam.send(embed=embed)


####    EPIC GAMES LOOP #


params_epic = {
    "platform": "epic-games-store",
    "type": "game"
}

response_epic = requests.get(url="https://www.gamerpower.com/api/giveaways", params=params_epic)
giveaways_epic = response_epic.json()

for i in range(len(giveaways_epic)):

    embed = Embed(
        title=giveaways_epic[i]["title"],
        description=f"{giveaways_epic[i]['worth']}\n{giveaways_epic[0]["end_date"].split()[0]}\n{giveaways_epic[0]["open_giveaway_url"]}",
    )
    embed.set_image(url=giveaways_epic[i]["image"])


    webhook_steam = SyncWebhook.from_url(EPICGAMES)
    webhook_steam.send(embed=embed)











