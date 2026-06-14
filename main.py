import requests
from discord import SyncWebhook,Embed
import os
from datetime import datetime



OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API")
WEBHOOK_KEY = os.environ.get("WEBHOOK")

###################################### FREE GAME ###################################### START
STEAM = os.environ.get("STEAM")
EPICGAMES = os.environ.get("EPICGAMES")
##################################### FREE GAME ####################################### END


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

###################################################### FREE GAME ALERT ############################################

#                                                          START                                                 #

################################################### Steam Free games loop #######################################
params = {
    "platform": "steam",
    "type": "game"
}

response_steam = requests.get(url="https://www.gamerpower.com/api/giveaways", params=params)
giveaways_steam = response_steam.json()

now_unix = int(datetime.timestamp(datetime.now()))

steam_message_id = 1515268058627706952

embed_steam = [Embed(
    title="🎮 Steam Free Games",
    description=f"Current Steam giveaways ({len(giveaways_steam)})\n"
                f"Last updated: <t:{now_unix}:R> ",

)]


for giveaway in giveaways_steam:
    end_date = giveaway["end_date"]
    dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    unix_timestamp = int(dt.timestamp())
    embed = Embed(
        title=giveaway["title"],
        description=(
            f"💰 {giveaway['worth']}\n"
            f"📅 Ends <t:{unix_timestamp}:R>\n"
            f"🔗 {giveaway['open_giveaway_url']}"
        )
    )
    embed.set_image(url=giveaway["image"])
    embed_steam.append(embed)

requests.patch(
    f"{STEAM}/messages/{steam_message_id}",
    json={"embeds": [embed.to_dict() for embed in embed_steam]},
)



################################################    EPIC GAMES LOOP #################################################


epic_message_id = 1515273389370249247

params_epic = {
    "platform": "epic-games-store",
    "type": "game"
}

response_epic = requests.get(url="https://www.gamerpower.com/api/giveaways", params=params_epic)
giveaways_epic = response_epic.json()

embed_epicgames = [Embed(
    title="🎮 EpicGames Free Games",
    description=f"Current EpicGames giveaways ({len(giveaways_epic)})\n"
                f"Last updated: <t:{now_unix}:R> ",

)]


for giveaway in giveaways_epic:
    end_date = giveaway["end_date"]
    dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    unix_timestamp = int(dt.timestamp())
    embed = Embed(
        title=giveaway["title"],
        description=(
            f"💰 {giveaway['worth']}\n"
            f"📅 Ends <t:{unix_timestamp}:R>\n"
            f"🔗 {giveaway['open_giveaway_url']}"
        )
    )
    embed.set_image(url=giveaway["image"])
    embed_epicgames.append(embed)

requests.patch(
    f"{EPICGAMES}/messages/{epic_message_id}",
    json={"embeds": [embed.to_dict() for embed in embed_epicgames]},
)












