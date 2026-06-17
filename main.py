import requests
from discord import SyncWebhook,Embed
import os
from datetime import datetime


SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_URL = os.environ.get("SHEETY_URL")

###################################### FREE GAME ###################################### START
STEAM = os.environ.get("STEAM")
EPICGAMES = os.environ.get("EPICGAMES")
##################################### FREE GAME ####################################### END


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

    webhook_send = SyncWebhook.from_url(url=url)
    webhook_send.send(embed=embed)

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













