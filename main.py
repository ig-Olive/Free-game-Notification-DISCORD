import requests
from discord import SyncWebhook, Embed
import os
import json
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

STEAM    = os.environ.get("STEAM")
EPICGAMES = os.environ.get("EPICGAMES")
ALLGAMES = os.environ.get("ALLGAMES")

# ── Auth ───────────────────────────────────────────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_info(
    json.loads(os.environ["GOOGLE_CREDENTIALS"]),
    scopes=SCOPES
)
client = gspread.authorize(creds)

sheet    = client.open_by_url(os.environ["SHEET_URL"])
steam_ws = sheet.worksheet("steamdatas")
epic_ws  = sheet.worksheet("epicdatas")
allgames_ws = sheet.worksheet("allgames")

# ── Sheet helpers (replaces Sheety) ───────────────────────────────────────────

def get_stored_game_ids(ws):
    values = ws.col_values(1)      # all values in column A
    return [int(v) for v in values[1:] if v]   # skip header, cast to int

def save_game_id(game_id, ws):
    ws.append_row([game_id])

def game_data_delete(row_id, ws):
    ws.delete_rows(row_id)         # row_id is 1-indexed (row 1 = header)

# ── Discord ────────────────────────────────────────────────────────────────────

def send_discord_message(giveaway, url):
    end_date = giveaway["end_date"]

    if end_date and end_date != "N/A":
        dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        end_str = f"<t:{int(dt.timestamp())}:R>"
    else:
        end_str = "No expiry date"

    embed = Embed(
        title=giveaway["title"],
        description=(
            f"💰 {giveaway['worth']}\n"
            f"📅 Ends {end_str}\n"
            f"🔗 {giveaway['open_giveaway_url']}"
        )
    )
    embed.set_image(url=giveaway["image"])
    SyncWebhook.from_url(url=url).send(embed=embed)

# ── Shared logic ───────────────────────────────────────────────────────────────

def update_data(free_games, stored_games, ws):
    """Remove game IDs from the sheet that are no longer free."""
    index = -1
    for game_id in stored_games:
        index += 1
        if game_id not in free_games:
            game_data_delete(index + 2, ws)  # +2: skip header + 1-indexed
            index -= 1                        # row shifted up after delete

def send_new_to_discord(giveaways, free_ids, stored_ids, webhook_url):
    """Send Discord alert only for games not already stored."""
    for i, game_id in enumerate(free_ids):
        if game_id not in stored_ids:
            send_discord_message(giveaways[i], webhook_url)

def store_new_games(free_games, stored_games, ws):
    """Append game IDs that aren't already in the sheet."""
    for game_id in free_games:
        if game_id not in stored_games:
            save_game_id(game_id, ws)

# ── Steam ──────────────────────────────────────────────────────────────────────

giveaways_steam     = requests.get(
    "https://www.gamerpower.com/api/giveaways",
    params={"platform": "steam", "type": "game"}
).json()

free_ids_steam      = [g["id"] for g in giveaways_steam]
stored_ids_steam    = get_stored_game_ids(steam_ws)

update_data(free_ids_steam, stored_ids_steam, steam_ws)
send_new_to_discord(giveaways_steam, free_ids_steam, stored_ids_steam, STEAM)
store_new_games(free_ids_steam, stored_ids_steam, steam_ws)

# ── Epic Games ─────────────────────────────────────────────────────────────────

giveaways_epic      = requests.get(
    "https://www.gamerpower.com/api/giveaways",
    params={"platform": "epic-games-store", "type": "game"}
).json()

free_ids_epic       = [g["id"] for g in giveaways_epic]
stored_ids_epic     = get_stored_game_ids(epic_ws)

update_data(free_ids_epic, stored_ids_epic, epic_ws)
send_new_to_discord(giveaways_epic, free_ids_epic, stored_ids_epic, EPICGAMES)
store_new_games(free_ids_epic, stored_ids_epic, epic_ws)

# ── All Games (excluding Steam & Epic) ────────────────────────────────────────

giveaways_all = requests.get(
    "https://www.gamerpower.com/api/giveaways",
    params={"platform": "pc", "type": "game"}
).json()

# Exclude Steam & Epic since they're already handled
excluded_ids = set(free_ids_steam + free_ids_epic)
giveaways_allgames = [g for g in giveaways_all if g["id"] not in excluded_ids]

free_ids_allgames   = [g["id"] for g in giveaways_allgames]
stored_ids_allgames = get_stored_game_ids(allgames_ws)

update_data(free_ids_allgames, stored_ids_allgames, allgames_ws)
send_new_to_discord(giveaways_allgames, free_ids_allgames, stored_ids_allgames, ALLGAMES)
store_new_games(free_ids_allgames, stored_ids_allgames, allgames_ws)
