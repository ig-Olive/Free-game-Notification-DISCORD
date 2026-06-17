import requests
from discord import SyncWebhook,Embed
import os
from datetime import datetime



OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API")
WEBHOOK_KEY = os.environ.get("WEBHOOK")
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_URL = os.environ.get("SHEETY_URL")

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
def get_stored_game_ids(platform):
    response = requests.get(url=f"{SHEETY_URL}/{platform}",headers={"Authorization":f"Bearer {SHEETY_TOKEN}"})
    response.raise_for_status()

    datas = response.json()[platform]
    return [(row["gameId"]) for row in datas]


def save_game_id(game_id,platform):
    payload = {
        platform[:-1]:{
            "gameId": game_id,
        }
    }

    response = requests.post(url=f"{SHEETY_URL}/{platform}", json=payload,headers={"Authorization":f"Bearer {SHEETY_TOKEN}"})
    response.raise_for_status()


def send_discord_message(giveaway,url):
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

    webhook = SyncWebhook.from_url(url=url)
    webhook.send(embed=embed)

def game_data_delete(row_id,platform):
    response = requests.delete(
        f"{SHEETY_URL}/{platform}/{row_id}",
        headers={
            "Authorization": f"Bearer {SHEETY_TOKEN}"
        }
    )
    response.raise_for_status()



#################################################### Steam Free games loop #################################

params = {
    "platform": "steam",
    "type": "game"
}

response_steam = requests.get(url="https://www.gamerpower.com/api/giveaways", params=params)
giveaways_steam = response_steam.json()




free_game_ids_steam = [giveaway["id"] for giveaway in giveaways_steam]

stored_game_ids_steam = get_stored_game_ids(platform="steamdatas")


def update_data(free_games, stored_games):
    index = -1
    for game_id in stored_games:
        index += 1
        if game_id not in free_games:
            game_data_delete(index+2,platform="steamdatas")
            index -= 1

def send_to_discord_steam():
    index = -1
    for game_id in free_game_ids_steam:
        index += 1
        if game_id not in stored_game_ids_steam:
            send_discord_message(giveaways_steam[index],STEAM)


def store_new_games(free_games,stored_games,platform):
    for game_id in free_games:
        if game_id not in stored_games:
            save_game_id(game_id,platform)




update_data(free_games=free_game_ids_steam, stored_games=stored_game_ids_steam)
send_to_discord_steam()
store_new_games(free_games=free_game_ids_steam,stored_games=stored_game_ids_steam,platform="steamdatas")





# ################################################    EPIC GAMES LOOP #################################################

params_epic = {
    "platform": "epic-games-store",
    "type": "game"
}

response_epic = requests.get(url="https://www.gamerpower.com/api/giveaways", params=params_epic)
giveaways_epic = response_epic.json()

free_game_ids_epic = [giveaway["id"] for giveaway in giveaways_epic]

stored_game_ids_epic = get_stored_game_ids(platform="epicdatas")


def update_data(free_games, stored_games):
    index = -1
    for game_id in stored_games:
        index += 1
        if game_id not in free_games:
            game_data_delete(index+2,platform="epicdatas")
            index -= 1

def send_to_discord_epic():
    index = -1
    for game_id in free_game_ids_epic:
        index += 1
        if game_id not in stored_game_ids_epic:
            send_discord_message(giveaways_epic[index],EPICGAMES)


def store_new_games(free_games,stored_games,platform):
    for game_id in free_games:
        if game_id not in stored_games:
            save_game_id(game_id,platform)




update_data(free_games=free_game_ids_epic, stored_games=stored_game_ids_epic)
send_to_discord_epic()
store_new_games(free_games=free_game_ids_epic,stored_games=stored_game_ids_epic,platform="epicdatas")













