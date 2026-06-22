#fucknigger4356789999999999
import asyncio
import html
import io
import json
import os
import random
import re
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional, Union

import discord
from dotenv import load_dotenv

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    Image = None
    ImageDraw = None
    ImageFont = None
    ImageFilter = None


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
DATA_DIR = BASE_DIR / "data"
SCORES_PATH = DATA_DIR / "scores.json"
STATCARDS_PATH = DATA_DIR / "statcards.json"
PROFILES_PATH = DATA_DIR / "profiles.json"
ROUND_ROBIN_PATH = DATA_DIR / "round_robin.json"
UNDO_PATH = DATA_DIR / "undo_stack.json"
SETTINGS_PATH = DATA_DIR / "settings.json"
TOURNAMENTS_PATH = DATA_DIR / "tournaments.json"
ASSETS_DIR = BASE_DIR / "assets"
TOURNAMENT_INVITE_ICON_PATH = ASSETS_DIR / "tournament_invite_icon.png"
TOURNAMENT_INVITE_ICON_NAME = "tournament_invite_icon.png"
EMBED_ICON_PATH = ASSETS_DIR / "embed_icon.png"
EMBED_ICON_NAME = "embed_icon.png"
TournamentPostChannel = Union[discord.TextChannel, discord.Thread, discord.ForumChannel]

SCORE_PER_PERCENT = 1000
LEADERBOARD_NAME = "\u2B50 Prestige Leaderboard \u2B50"
RANK_MEDALS = {
    1: "\U0001F947",
    2: "\U0001F948",
    3: "\U0001F949",
}
RANK_SPACER = "<:_:0>"

EMBED_COLOR = discord.Color.from_rgb(126, 49, 255)
SUCCESS_COLOR = EMBED_COLOR
ERROR_COLOR = EMBED_COLOR

CLANS = [
    "None",
    "Orfeo - Squadra Orfeo",
    "KO - KnockOut",
    "WH\u03A3 - White Eminence",
    "KS - Knights Shadows",
    "ND - Nemesis Domain",
    "P11 - Penguin Eleven",
    "LRK - Last Resort Kingdom",
    "ATR - Altair",
    "IBE - Inazuma Battle Eleven",
    "TR - The Resistance",
    "SYC - Sycel Esports",
    "FGS - Flaming Spear",
    "FK\u00C6 - Football Klub \u00C6on",
    "HC - Heaven Chaos",
    "LZ - Last Zodiacs",
    "Order - The Order",
    "N\u00F82 - Nuevo Orden 2",
    "TN - Tormenta Nocturna",
    "HsK - Heaven's Karma",
    "(L\u00A7) - Luna Sangrienta",
    "TRE - Tenchi Raimei Esport",
    "LR - La Resurrecci\u00F3n",
    "DR - Doux R\u00EAveurs",
    "FF - Ocean Drifters FF",
    "JF - Juicio Final",
    "RG - Royaume Gamidonique",
    "ZERO - Team Zero",
    "QYK - Quymera Kaiser",
    "SIX - Secret Iberix",
    "UY\u03A9 - Unity Lock",
    "KCT - Kaminari Crows Team",
    "GH - GEEKHIT",
    "GVE - Good Vibes E-sport",
    "NV - Nova E-sport",
    "VZ - Virtual Zero",
    "RD - Resistance Dragon",
    "COP - Coppetta",
    "AVN - Avalon",
    "SOD - Samurai of Destiny",
    "NKO - Nokotta FC",
    "ELD - Eldorado",
    "LC - LaCelesta",
    "OMN - TEAM OMNIA",
    "RGG - RaGGers",
    "KK - Krolewskie Koty",
    "AR17 - Aruges17 Team",
]
COUNTRIES = {
    "Afghanistan": "AF", "Albania": "AL", "Algeria": "DZ", "Andorra": "AD", "Angola": "AO",
    "Antigua and Barbuda": "AG", "Argentina": "AR", "Armenia": "AM", "Australia": "AU", "Austria": "AT",
    "Azerbaijan": "AZ", "Bahamas": "BS", "Bahrain": "BH", "Bangladesh": "BD", "Barbados": "BB",
    "Belarus": "BY", "Belgium": "BE", "Belize": "BZ", "Benin": "BJ", "Bhutan": "BT",
    "Bolivia": "BO", "Bosnia and Herzegovina": "BA", "Botswana": "BW", "Brazil": "BR", "Brunei": "BN",
    "Bulgaria": "BG", "Burkina Faso": "BF", "Burundi": "BI", "Cabo Verde": "CV", "Cambodia": "KH",
    "Cameroon": "CM", "Canada": "CA", "Central African Republic": "CF", "Chad": "TD", "Chile": "CL",
    "China": "CN", "Colombia": "CO", "Comoros": "KM", "Congo": "CG", "Costa Rica": "CR", "Cote d'Ivoire": "CI",
    "Croatia": "HR", "Cuba": "CU", "Cyprus": "CY", "Czechia": "CZ", "Denmark": "DK",
    "Djibouti": "DJ", "Dominica": "DM", "Dominican Republic": "DO", "Ecuador": "EC", "Egypt": "EG",
    "El Salvador": "SV", "Equatorial Guinea": "GQ", "Eritrea": "ER", "Estonia": "EE", "Eswatini": "SZ",
    "Ethiopia": "ET", "Fiji": "FJ", "Finland": "FI", "France": "FR", "Gabon": "GA",
    "Gambia": "GM", "Georgia": "GE", "Germany": "DE", "Ghana": "GH", "Greece": "GR",
    "Grenada": "GD", "Guatemala": "GT", "Guinea": "GN", "Guinea-Bissau": "GW", "Guyana": "GY",
    "Haiti": "HT", "Honduras": "HN", "Hungary": "HU", "Iceland": "IS", "India": "IN",
    "Indonesia": "ID", "Iran": "IR", "Iraq": "IQ", "Ireland": "IE", "Israel": "IL",
    "Italy": "IT", "Jamaica": "JM", "Japan": "JP", "Jordan": "JO", "Kazakhstan": "KZ",
    "Kenya": "KE", "Kiribati": "KI", "Kuwait": "KW", "Kyrgyzstan": "KG", "Laos": "LA",
    "Latvia": "LV", "Lebanon": "LB", "Lesotho": "LS", "Liberia": "LR", "Libya": "LY",
    "Liechtenstein": "LI", "Lithuania": "LT", "Luxembourg": "LU", "Madagascar": "MG", "Malawi": "MW",
    "Malaysia": "MY", "Maldives": "MV", "Mali": "ML", "Malta": "MT", "Marshall Islands": "MH",
    "Mauritania": "MR", "Mauritius": "MU", "Mexico": "MX", "Micronesia": "FM", "Moldova": "MD",
    "Monaco": "MC", "Mongolia": "MN", "Montenegro": "ME", "Morocco": "MA", "Mozambique": "MZ",
    "Myanmar": "MM", "Namibia": "NA", "Nauru": "NR", "Nepal": "NP", "Netherlands": "NL",
    "New Zealand": "NZ", "Nicaragua": "NI", "Niger": "NE", "Nigeria": "NG", "North Korea": "KP",
    "North Macedonia": "MK", "Norway": "NO", "Oman": "OM", "Pakistan": "PK", "Palau": "PW",
    "Palestine": "PS", "Panama": "PA", "Papua New Guinea": "PG", "Paraguay": "PY", "Peru": "PE",
    "Philippines": "PH", "Poland": "PL", "Portugal": "PT", "Qatar": "QA", "Romania": "RO",
    "Russia": "RU", "Rwanda": "RW", "Saint Kitts and Nevis": "KN", "Saint Lucia": "LC",
    "Saint Vincent and the Grenadines": "VC", "Samoa": "WS", "San Marino": "SM", "Sao Tome and Principe": "ST",
    "Saudi Arabia": "SA", "Senegal": "SN", "Serbia": "RS", "Seychelles": "SC", "Sierra Leone": "SL",
    "Singapore": "SG", "Slovakia": "SK", "Slovenia": "SI", "Solomon Islands": "SB", "Somalia": "SO",
    "South Africa": "ZA", "South Korea": "KR", "South Sudan": "SS", "Spain": "ES", "Sri Lanka": "LK",
    "Sudan": "SD", "Suriname": "SR", "Sweden": "SE", "Switzerland": "CH", "Syria": "SY",
    "Taiwan": "TW", "Tajikistan": "TJ", "Tanzania": "TZ", "Thailand": "TH", "Timor-Leste": "TL",
    "Togo": "TG", "Tonga": "TO", "Trinidad and Tobago": "TT", "Tunisia": "TN", "Turkey": "TR",
    "Turkmenistan": "TM", "Tuvalu": "TV", "Uganda": "UG", "Ukraine": "UA", "United Arab Emirates": "AE",
    "United Kingdom": "GB", "United States": "US", "Uruguay": "UY", "Uzbekistan": "UZ", "Vanuatu": "VU",
    "Vatican City": "VA", "Venezuela": "VE", "Vietnam": "VN", "Yemen": "YE", "Zambia": "ZM", "Zimbabwe": "ZW",
}

COUNTRY_ALIASES = {
    "america": "United States",
    "britain": "United Kingdom",
    "czech republic": "Czechia",
    "england": "United Kingdom",
    "holland": "Netherlands",
    "ivory coast": "Cote d'Ivoire",
    "korea": "South Korea",
    "scotland": "United Kingdom",
    "the netherlands": "Netherlands",
    "uk": "United Kingdom",
    "united states of america": "United States",
    "usa": "United States",
    "us": "United States",
    "wales": "United Kingdom",
}

load_dotenv(ENV_PATH)

TOKEN = os.getenv("DISCORD_TOKEN")
CHALLONGE_API_KEY = os.getenv("CHALLONGE_API_KEY")
CHALLONGE_ACCESS_TOKEN = os.getenv("CHALLONGE_ACCESS_TOKEN")
CHALLONGE_CLIENT_ID = os.getenv("CHALLONGE_CLIENT_ID")
CHALLONGE_CLIENT_SECRET = os.getenv("CHALLONGE_CLIENT_SECRET")
CHALLONGE_COMMUNITY_ID = os.getenv("CHALLONGE_COMMUNITY_ID")
CHALLONGE_REDIRECT_URI = os.getenv("CHALLONGE_REDIRECT_URI")
CHALLONGE_API_BASE_URL = "https://api.challonge.com/v2.1"
CHALLONGE_V1_BASE_URL = "https://api.challonge.com/v1"
CHALLONGE_AUTHORIZE_URL = "https://api.challonge.com/oauth/authorize"
CHALLONGE_TOKEN_URL = "https://api.challonge.com/oauth/token"
CHALLONGE_USER_AGENT = "CFI-Endgame-Discord-Bot/1.0 Mozilla/5.0"
CHALLONGE_SCOPES = "me tournaments:read tournaments:write matches:read matches:write participants:read participants:write"

if not TOKEN or TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE":
    raise SystemExit(
        "Missing Discord bot token.\n"
        "Open C:\\discord-bot\\.env and set:\n"
        "DISCORD_TOKEN=your_real_bot_token_here"
    )

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
MATCH_VOTES = {}
NEXT_MATCH_ID = 1
TOURNAMENT_LOCK = asyncio.Lock()
CHALLONGE_TOKEN_CACHE = {"access_token": None, "expires_at": 0}


def load_scores():
    if not SCORES_PATH.exists():
        return {}

    with SCORES_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_scores(scores):
    DATA_DIR.mkdir(exist_ok=True)

    with SCORES_PATH.open("w", encoding="utf-8") as file:
        json.dump(scores, file, indent=2)


def load_statcards():
    if not STATCARDS_PATH.exists():
        return {}

    with STATCARDS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_statcards(statcards):
    DATA_DIR.mkdir(exist_ok=True)

    with STATCARDS_PATH.open("w", encoding="utf-8") as file:
        json.dump(statcards, file, indent=2, ensure_ascii=False)


def load_profiles():
    if not PROFILES_PATH.exists():
        return {}

    with PROFILES_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_profiles(profiles):
    DATA_DIR.mkdir(exist_ok=True)

    with PROFILES_PATH.open("w", encoding="utf-8") as file:
        json.dump(profiles, file, indent=2, ensure_ascii=False)


def load_round_robin():
    if not ROUND_ROBIN_PATH.exists():
        return {"played_pairs": [], "round": 0, "current_players": [], "current_pairings": [], "player_names": {}}

    try:
        with ROUND_ROBIN_PATH.open("r", encoding="utf-8") as file:
            round_robin = json.load(file)
    except json.JSONDecodeError:
        backup_path = ROUND_ROBIN_PATH.with_suffix(".json.broken")
        ROUND_ROBIN_PATH.replace(backup_path)
        print(f"round_robin.json was corrupted and has been moved to {backup_path}")
        return {"played_pairs": [], "round": 0, "current_players": [], "current_pairings": []}

    round_robin.setdefault("played_pairs", [])
    round_robin.setdefault("round", 0)
    round_robin.setdefault("current_players", [])
    round_robin.setdefault("current_pairings", [])
    round_robin.setdefault("player_names", {})

    if not round_robin["current_pairings"] and round_robin["played_pairs"]:
        latest_pair_keys = round_robin["played_pairs"][-5:]
        recovered_pairings = []

        for saved_pair in latest_pair_keys:
            player_ids = saved_pair.split("-", 1)

            if len(player_ids) == 2:
                recovered_pairings.append(player_ids)

        recovered_players = []

        for player_one_id, player_two_id in recovered_pairings:
            if player_one_id not in recovered_players:
                recovered_players.append(player_one_id)
            if player_two_id not in recovered_players:
                recovered_players.append(player_two_id)

        round_robin["current_pairings"] = recovered_pairings
        round_robin["current_players"] = recovered_players

    return round_robin


def save_round_robin(round_robin):
    DATA_DIR.mkdir(exist_ok=True)

    with ROUND_ROBIN_PATH.open("w", encoding="utf-8") as file:
        json.dump(round_robin, file, indent=2)


def load_undo_stack():
    if not UNDO_PATH.exists():
        return []

    try:
        with UNDO_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        backup_path = UNDO_PATH.with_suffix(".json.broken")
        UNDO_PATH.replace(backup_path)
        print(f"undo_stack.json was corrupted and has been moved to {backup_path}")
        return []


def save_undo_stack(undo_stack):
    DATA_DIR.mkdir(exist_ok=True)

    with UNDO_PATH.open("w", encoding="utf-8") as file:
        json.dump(undo_stack[-25:], file, indent=2, ensure_ascii=False)


def record_undo(action, scores=None, statcards=None, profiles=None, round_robin=None, tournaments=None):
    undo_stack = load_undo_stack()
    undo_stack.append({
        "action": action,
        "scores": scores,
        "statcards": statcards,
        "profiles": profiles,
        "round_robin": round_robin,
        "tournaments": tournaments,
    })
    save_undo_stack(undo_stack)


def load_settings():
    if not SETTINGS_PATH.exists():
        return {}

    with SETTINGS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_settings(settings):
    DATA_DIR.mkdir(exist_ok=True)

    with SETTINGS_PATH.open("w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2)


def load_tournaments():
    if not TOURNAMENTS_PATH.exists():
        return {"active_id": None, "active_by_guild": {}, "next_id": 1, "tournaments": {}}

    try:
        with TOURNAMENTS_PATH.open("r", encoding="utf-8") as file:
            tournaments = json.load(file)
    except json.JSONDecodeError:
        backup_path = TOURNAMENTS_PATH.with_suffix(".json.broken")
        TOURNAMENTS_PATH.replace(backup_path)
        print(f"tournaments.json was corrupted and has been moved to {backup_path}")
        return {"active_id": None, "active_by_guild": {}, "next_id": 1, "tournaments": {}}

    tournaments.setdefault("active_id", None)
    tournaments.setdefault("active_by_guild", {})
    tournaments.setdefault("next_id", 1)
    tournaments.setdefault("tournaments", {})
    return tournaments


def save_tournaments(tournaments):
    DATA_DIR.mkdir(exist_ok=True)

    with TOURNAMENTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(tournaments, file, indent=2, ensure_ascii=False)


def request_challonge_token(form_data):
    body = urllib.parse.urlencode(form_data).encode("utf-8")
    request = urllib.request.Request(
        CHALLONGE_TOKEN_URL,
        data=body,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": CHALLONGE_USER_AGENT,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body) if response_body else {}
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        if "browser_signature_banned" in error_body or "error-1010" in error_body:
            raise RuntimeError(
                "Challonge blocked the OAuth request with Cloudflare browser-signature protection."
            ) from error
        raise RuntimeError(f"Challonge OAuth error {error.code}: {error_body}") from error


def save_challonge_oauth_tokens(token_data):
    access_token = token_data.get("access_token")

    if not access_token:
        raise RuntimeError(f"Challonge OAuth did not return an access token: {token_data}")

    settings = load_settings()
    expires_in = int(token_data.get("expires_in", 604800))
    settings["challonge_oauth"] = {
        "access_token": access_token,
        "refresh_token": token_data.get("refresh_token"),
        "expires_at": time.time() + expires_in,
        "scope": token_data.get("scope", ""),
    }
    save_settings(settings)
    CHALLONGE_TOKEN_CACHE["access_token"] = access_token
    CHALLONGE_TOKEN_CACHE["expires_at"] = settings["challonge_oauth"]["expires_at"]


def refresh_challonge_oauth_token(refresh_token):
    token_data = request_challonge_token({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CHALLONGE_CLIENT_ID,
        "client_secret": CHALLONGE_CLIENT_SECRET,
    })
    save_challonge_oauth_tokens(token_data)
    return token_data["access_token"]


def get_challonge_oauth_token(use_client_credentials=False):
    if CHALLONGE_ACCESS_TOKEN:
        return CHALLONGE_ACCESS_TOKEN

    settings = load_settings()
    saved_oauth = settings.get("challonge_oauth", {})
    saved_token = saved_oauth.get("access_token")
    saved_expires_at = float(saved_oauth.get("expires_at", 0) or 0)

    if saved_token and saved_expires_at > time.time() + 60:
        return saved_token

    if saved_oauth.get("refresh_token") and CHALLONGE_CLIENT_ID and CHALLONGE_CLIENT_SECRET:
        return refresh_challonge_oauth_token(saved_oauth["refresh_token"])

    if not use_client_credentials:
        return None

    if not CHALLONGE_CLIENT_ID or not CHALLONGE_CLIENT_SECRET:
        return None

    now = time.time()

    if CHALLONGE_TOKEN_CACHE["access_token"] and CHALLONGE_TOKEN_CACHE["expires_at"] > now + 60:
        return CHALLONGE_TOKEN_CACHE["access_token"]

    token_data = request_challonge_token({
        "grant_type": "client_credentials",
        "client_id": CHALLONGE_CLIENT_ID,
        "client_secret": CHALLONGE_CLIENT_SECRET,
        "scope": CHALLONGE_SCOPES,
    })

    access_token = token_data.get("access_token")

    if not access_token:
        raise RuntimeError(f"Challonge OAuth did not return an access token: {token_data}")

    expires_in = int(token_data.get("expires_in", 3600))
    CHALLONGE_TOKEN_CACHE["access_token"] = access_token
    CHALLONGE_TOKEN_CACHE["expires_at"] = now + expires_in
    return access_token


def challonge_auth_headers():
    if CHALLONGE_API_KEY:
        return {
            "Authorization-Type": "v1",
            "Authorization": CHALLONGE_API_KEY,
        }

    access_token = get_challonge_oauth_token()

    if access_token:
        return {"Authorization": f"Bearer {access_token}"}

    raise RuntimeError(
        "Challonge credentials are missing. Add CHALLONGE_CLIENT_ID and CHALLONGE_CLIENT_SECRET "
        "or CHALLONGE_API_KEY to C:\\discord-bot\\.env"
    )


def challonge_request(method, path, payload=None, query=None):
    auth_headers = challonge_auth_headers()

    query = dict(query or {})

    if CHALLONGE_COMMUNITY_ID:
        query["community_id"] = CHALLONGE_COMMUNITY_ID

    query_string = ""

    if query:
        query_string = "?" + urllib.parse.urlencode(query)

    url = f"{CHALLONGE_API_BASE_URL}{path}{query_string}"
    body = None
    headers = {
        "Accept": "application/json",
        "User-Agent": CHALLONGE_USER_AGENT,
    }
    headers.update(auth_headers)

    if payload is not None:
        headers["Content-Type"] = "application/vnd.api+json"
        body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body) if response_body else {}
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        if "browser_signature_banned" in error_body or "error-1010" in error_body:
            raise RuntimeError(
                "Challonge blocked the API request with Cloudflare browser-signature protection. "
                "If this continues, we may need to use an API v1 key or host the bot somewhere Challonge accepts."
            ) from error
        if error.code == 401:
            raise RuntimeError(
                "Challonge rejected the saved authorization token.\n\n"
                f"Details: {error_body[:1200]}\n\n"
                "Try restarting the bot first. If it still fails, run `/challonge_auth_url` and "
                "`/challonge_auth_finish` again so Challonge re-approves the current app permissions."
            ) from error
        raise RuntimeError(f"Challonge API error {error.code}: {error_body}") from error


async def challonge_request_async(method, path, payload=None, query=None):
    return await asyncio.to_thread(challonge_request, method, path, payload, query)


def challonge_tournament_url(challonge_data):
    data = challonge_data.get("data", {})
    attributes = data.get("attributes", {})

    for key in ["full_challonge_url", "live_image_url", "url"]:
        value = attributes.get(key)

        if value and str(value).startswith("http"):
            return value

    slug = attributes.get("url") or attributes.get("slug")

    if slug:
        return f"https://challonge.com/{slug}"

    tournament_id = data.get("id")

    return f"https://challonge.com/{tournament_id}" if tournament_id else None


async def create_challonge_tournament(tournament, private=False, url_slug=None):
    attributes = {
        "name": tournament["name"],
        "tournament_type": "single elimination",
        "private": private,
        "description": "Created from the CFI Discord bot.",
    }

    if url_slug:
        attributes["url"] = url_slug

    payload = {
        "data": {
            "type": "tournament",
            "attributes": attributes,
        }
    }
    return await challonge_request_async("POST", "/tournaments.json", payload)


async def bulk_create_challonge_participants(challonge_tournament_id, players):
    participants = [
        {
            "name": player.get("name") or f"Player {index}",
            "seed": index,
            "misc": player.get("id", ""),
        }
        for index, player in enumerate(players, start=1)
    ]

    if not participants:
        return {"data": []}

    payload = {
        "data": {
            "type": "Participants",
            "attributes": {
                "participants": participants,
            },
        }
    }
    return await challonge_request_async(
        "POST",
        f"/tournaments/{challonge_tournament_id}/participants/bulk_add.json",
        payload,
    )


def challonge_v1_request(method, path, form=None, query=None):
    if not CHALLONGE_API_KEY:
        raise RuntimeError("Add `CHALLONGE_API_KEY=your_key_here` to `C:\\discord-bot\\.env`, then restart the bot.")

    form_items = list(form or [])
    query_items = list(query or [])

    if method.upper() in {"GET", "DELETE"}:
        query_items.append(("api_key", CHALLONGE_API_KEY))
    else:
        form_items.append(("api_key", CHALLONGE_API_KEY))

    query_string = ""

    if query_items:
        query_string = "?" + urllib.parse.urlencode(query_items)

    url = f"{CHALLONGE_V1_BASE_URL}{path}{query_string}"
    body = None
    headers = {
        "Accept": "application/json",
        "User-Agent": CHALLONGE_USER_AGENT,
    }

    if form_items:
        body = urllib.parse.urlencode(form_items).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    request = urllib.request.Request(url, data=body, headers=headers, method=method.upper())

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body) if response_body else {}
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        if error.code == 401:
            raise RuntimeError("Challonge rejected the API v1 key. Check `CHALLONGE_API_KEY` in `.env`, restart, and try again.") from error
        raise RuntimeError(f"Challonge API v1 error {error.code}: {error_body[:1200]}") from error


async def challonge_v1_request_async(method, path, form=None, query=None):
    return await asyncio.to_thread(challonge_v1_request, method, path, form, query)


def challonge_v1_tournament_url(response_data):
    tournament = response_data.get("tournament", response_data)

    for key in ["full_challonge_url", "live_image_url"]:
        value = tournament.get(key)

        if value:
            return value

    slug = tournament.get("url")

    if slug:
        return f"https://challonge.com/{slug}"

    tournament_id = tournament.get("id")
    return f"https://challonge.com/{tournament_id}" if tournament_id else None


def challonge_v1_tournament_identifier(response_data):
    tournament = response_data.get("tournament", response_data)
    return str(tournament.get("url") or tournament.get("id") or "")


def challonge_v1_tournament_numeric_id(response_data):
    tournament = response_data.get("tournament", response_data)
    tournament_id = tournament.get("id")
    return str(tournament_id) if tournament_id else ""


def challonge_slug_from_url(url):
    normalized_url = normalize_challonge_url(url)

    if not normalized_url:
        return None

    parsed = urllib.parse.urlparse(normalized_url)
    path_parts = [part for part in parsed.path.split("/") if part]
    return path_parts[-1] if path_parts else None


def make_challonge_url_slug(tournament, preferred_slug=""):
    clean_slug = preferred_slug.strip().lower()

    if clean_slug:
        return "_".join(
            part
            for part in "".join(character if character.isalnum() or character == "_" else "_" for character in clean_slug).split("_")
            if part
        )

    name_slug = "".join(
        character.lower() if character.isalnum() else "_"
        for character in tournament.get("name", "cfi-tournament")
    ).strip("_")
    name_slug = "_".join(part for part in name_slug.split("_") if part)
    return f"{name_slug or 'cfi_tournament'}_{tournament.get('id', int(time.time()))}"


async def create_challonge_v1_tournament(tournament, private=False, url_slug=""):
    slug = make_challonge_url_slug(tournament, url_slug)
    form = [
        ("tournament[name]", tournament["name"]),
        ("tournament[url]", slug),
        ("tournament[tournament_type]", "single elimination"),
        ("tournament[private]", "1" if private else "0"),
        ("tournament[shuffle_seeds]", "0"),
        ("tournament[description]", "Created from the CFI Discord bot."),
    ]
    return await challonge_v1_request_async("POST", "/tournaments.json", form=form)


async def create_and_link_challonge_v1_tournament(tournament, private=False, url_slug=""):
    last_error = None
    preferred_slug = url_slug

    for attempt in range(5):
        retry_slug = preferred_slug

        if attempt and not preferred_slug:
            retry_slug = f"{make_challonge_url_slug(tournament)}_{int(time.time())}_{attempt}"
        elif attempt:
            retry_slug = f"{make_challonge_url_slug(tournament, preferred_slug)}_{int(time.time())}_{attempt}"

        try:
            challonge_tournament = await create_challonge_v1_tournament(tournament, private=private, url_slug=retry_slug)
            break
        except RuntimeError as error:
            last_error = str(error)

            if "taken" not in last_error.lower() and "url" not in last_error.lower():
                raise
    else:
        raise RuntimeError(last_error or "Challonge could not create a tournament.")

    tournament_identifier = challonge_v1_tournament_identifier(challonge_tournament)
    tournament_numeric_id = challonge_v1_tournament_numeric_id(challonge_tournament)

    if not tournament_identifier:
        raise RuntimeError(f"Challonge did not return a tournament identifier: {challonge_tournament}")

    api_identifier = tournament_numeric_id or tournament_identifier
    participants_response = await bulk_create_challonge_v1_participants(
        api_identifier,
        tournament.get("players", []),
    )
    participant_count = len(participants_response) if isinstance(participants_response, list) else len(tournament.get("players", []))
    participant_map = extract_challonge_v1_participant_map(participants_response, tournament.get("players", []))
    challonge_url = challonge_v1_tournament_url(challonge_tournament) or f"https://challonge.com/{tournament_identifier}"
    tournament["challonge"] = {
        "mode": "api_v1",
        "id": tournament_identifier,
        "numeric_id": tournament_numeric_id,
        "participant_ids": participant_map,
        "private": private,
        "url": challonge_url,
    }
    tournament["challonge_url"] = challonge_url
    return challonge_url, participant_count


async def start_challonge_v1_tournament(tournament_identifier):
    return await challonge_v1_request_async(
        "POST",
        f"/tournaments/{urllib.parse.quote(str(tournament_identifier), safe='')}/start.json",
        form=[],
    )


async def bulk_create_challonge_v1_participants(tournament_identifier, players):
    form = []

    for player in players:
        form.append(("participants[][name]", player.get("name") or f"Player {player.get('id', '')}".strip()))
        form.append(("participants[][misc]", str(player.get("id", ""))))

    if not form:
        return []

    return await challonge_v1_request_async(
        "POST",
        f"/tournaments/{urllib.parse.quote(str(tournament_identifier), safe='')}/participants/bulk_add.json",
        form=form,
    )


async def create_challonge_v1_participant(tournament_identifier, player):
    form = [
        ("participant[name]", player.get("name") or f"Player {player.get('id', '')}".strip()),
        ("participant[misc]", str(player.get("id", ""))),
    ]
    return await challonge_v1_request_async(
        "POST",
        f"/tournaments/{urllib.parse.quote(str(tournament_identifier), safe='')}/participants.json",
        form=form,
    )


async def sync_new_player_to_challonge(tournament, player):
    if tournament.get("status") != "setup":
        return None

    tournament_identifier = get_challonge_identifier_from_tournament(tournament)

    if not tournament_identifier or not CHALLONGE_API_KEY:
        return None

    if str(player.get("id")) in tournament.get("challonge", {}).get("participant_ids", {}):
        return "already_synced"

    participant_response = await create_challonge_v1_participant(tournament_identifier, player)
    participant = unwrap_challonge_v1_item(participant_response, "participant")
    participant_id = participant.get("id")

    if participant_id:
        tournament.setdefault("challonge", {}).setdefault("participant_ids", {})[str(player.get("id"))] = str(participant_id)

    return "synced"


async def ensure_setup_challonge_bracket(tournament):
    if tournament.get("challonge_url"):
        tournament.pop("challonge_error", None)
        return "already_linked"

    if not CHALLONGE_API_KEY:
        tournament["challonge_error"] = "API key missing"
        return "missing_key"

    if len(tournament.get("players", [])) < 2:
        tournament.pop("challonge_error", None)
        return "waiting_for_players"

    try:
        challonge_url, participant_count = await create_and_link_challonge_v1_tournament(tournament)
    except RuntimeError as error:
        tournament["challonge_error"] = str(error)
        raise

    tournament.pop("challonge_error", None)
    return ("created", challonge_url, participant_count)


async def list_challonge_v1_participants(tournament_identifier):
    return await challonge_v1_request_async(
        "GET",
        f"/tournaments/{urllib.parse.quote(str(tournament_identifier), safe='')}/participants.json",
    )


async def list_challonge_v1_matches(tournament_identifier):
    return await challonge_v1_request_async(
        "GET",
        f"/tournaments/{urllib.parse.quote(str(tournament_identifier), safe='')}/matches.json",
    )


async def update_challonge_v1_match(tournament_identifier, match_id, scores_csv, winner_id):
    form = [
        ("match[scores_csv]", scores_csv),
        ("match[winner_id]", str(winner_id)),
    ]
    return await challonge_v1_request_async(
        "PUT",
        f"/tournaments/{urllib.parse.quote(str(tournament_identifier), safe='')}/matches/{match_id}.json",
        form=form,
    )


async def reopen_challonge_v1_match(tournament_identifier, match_id):
    return await challonge_v1_request_async(
        "POST",
        f"/tournaments/{urllib.parse.quote(str(tournament_identifier), safe='')}/matches/{match_id}/reopen.json",
        form=[],
    )


async def delete_challonge_v1_participant(tournament_identifier, participant_id):
    return await challonge_v1_request_async(
        "DELETE",
        f"/tournaments/{urllib.parse.quote(str(tournament_identifier), safe='')}/participants/{participant_id}.json",
    )


def unwrap_challonge_v1_item(item, key):
    if isinstance(item, dict) and key in item and isinstance(item[key], dict):
        return item[key]

    return item if isinstance(item, dict) else {}


def extract_challonge_v1_participant_map(participants_response, tournament_players=None):
    participant_map = {}
    name_to_player_id = {}

    for player in tournament_players or []:
        player_name = str(player.get("name", "")).casefold()

        if player_name:
            name_to_player_id[player_name] = str(player.get("id"))

    for item in participants_response or []:
        participant = unwrap_challonge_v1_item(item, "participant")
        participant_id = participant.get("id")

        if not participant_id:
            continue

        misc = str(participant.get("misc") or "").strip()

        if misc:
            participant_map[misc] = str(participant_id)
            continue

        participant_name = str(participant.get("name") or "").casefold()
        matched_player_id = name_to_player_id.get(participant_name)

        if matched_player_id:
            participant_map[matched_player_id] = str(participant_id)

    return participant_map


def get_challonge_identifier_from_tournament(tournament):
    challonge = tournament.get("challonge", {})
    identifier = challonge.get("numeric_id") or challonge.get("id")

    if identifier:
        return str(identifier)

    url = tournament.get("challonge_url") or challonge.get("url")

    if url:
        return challonge_slug_from_url(url)

    return None


async def ensure_challonge_participant_map(tournament):
    challonge = tournament.setdefault("challonge", {})
    participant_map = challonge.get("participant_ids", {})

    if participant_map:
        return participant_map

    tournament_identifier = get_challonge_identifier_from_tournament(tournament)

    if not tournament_identifier:
        return {}

    participants_response = await list_challonge_v1_participants(tournament_identifier)
    participant_map = extract_challonge_v1_participant_map(participants_response, tournament.get("players", []))
    challonge["participant_ids"] = participant_map
    return participant_map


async def get_challonge_v1_matches_for_tournament(tournament):
    tournament_identifier = get_challonge_identifier_from_tournament(tournament)

    if not tournament_identifier:
        return None, None, "No Challonge tournament identifier is saved."

    try:
        matches_response = await list_challonge_v1_matches(tournament_identifier)
    except RuntimeError as error:
        challonge_slug = challonge_slug_from_url(tournament.get("challonge_url") or tournament.get("challonge", {}).get("url", ""))

        if challonge_slug and challonge_slug != str(tournament_identifier):
            try:
                matches_response = await list_challonge_v1_matches(challonge_slug)
                tournament.setdefault("challonge", {})["id"] = challonge_slug
                tournament.setdefault("challonge", {}).pop("numeric_id", None)
                tournament_identifier = challonge_slug
            except RuntimeError:
                return None, None, str(error)
        else:
            return None, None, str(error)

    return tournament_identifier, matches_response, None


async def find_challonge_v1_match_for_local_match(tournament, match):
    participant_map = await ensure_challonge_participant_map(tournament)
    player_one_id = str(match["player_one"]["id"])
    player_two_id = str(match["player_two"]["id"])
    challonge_player_one_id = participant_map.get(player_one_id)
    challonge_player_two_id = participant_map.get(player_two_id)

    if not challonge_player_one_id or not challonge_player_two_id:
        return None, None, "Could not match the Discord players to Challonge participants."

    tournament_identifier, matches_response, warning = await get_challonge_v1_matches_for_tournament(tournament)

    if warning:
        return None, None, warning

    target_match = None

    for item in matches_response or []:
        challonge_match = unwrap_challonge_v1_item(item, "match")
        match_player_ids = {
            str(challonge_match.get("player1_id")),
            str(challonge_match.get("player2_id")),
        }

        if match_player_ids == {challonge_player_one_id, challonge_player_two_id}:
            target_match = challonge_match
            break

    if not target_match:
        return None, None, "Could not find the matching match on Challonge."

    return tournament_identifier, target_match, None


async def sync_challonge_v1_score(tournament, match):
    tournament_identifier, target_match, warning = await find_challonge_v1_match_for_local_match(tournament, match)

    if warning:
        return warning

    score = match.get("score", {})
    participant_map = await ensure_challonge_participant_map(tournament)
    player_one_id = str(match["player_one"]["id"])
    player_two_id = str(match["player_two"]["id"])
    challonge_player_one_id = participant_map.get(player_one_id)
    challonge_player_two_id = participant_map.get(player_two_id)
    score_by_challonge_player = {
        challonge_player_one_id: score.get("player_one", 0),
        challonge_player_two_id: score.get("player_two", 0),
    }
    challonge_match_player_one_id = str(target_match.get("player1_id"))
    challonge_match_player_two_id = str(target_match.get("player2_id"))
    scores_csv = (
        f"{score_by_challonge_player.get(challonge_match_player_one_id, 0)}-"
        f"{score_by_challonge_player.get(challonge_match_player_two_id, 0)}"
    )
    winner_id = participant_map.get(str(match["winner"]["id"]))

    await update_challonge_v1_match(tournament_identifier, target_match["id"], scores_csv, winner_id)
    return None


async def reopen_challonge_v1_match_for_local_match(tournament, match):
    tournament_identifier, target_match, warning = await find_challonge_v1_match_for_local_match(tournament, match)

    if warning:
        return warning

    await reopen_challonge_v1_match(tournament_identifier, target_match["id"])
    return None


async def sync_removed_player_from_challonge(tournament, player_id):
    if tournament.get("status") != "setup":
        return None

    tournament_identifier = get_challonge_identifier_from_tournament(tournament)

    if not tournament_identifier or not CHALLONGE_API_KEY:
        return None

    participant_map = await ensure_challonge_participant_map(tournament)
    participant_id = participant_map.get(str(player_id))

    if not participant_id:
        return "Could not find that player as a Challonge participant."

    await delete_challonge_v1_participant(tournament_identifier, participant_id)
    tournament.setdefault("challonge", {}).setdefault("participant_ids", {}).pop(str(player_id), None)
    return None


def get_embed_icon_url():
    return client.user.display_avatar.url if client.user else None


def brand_embed(embed):
    embed.color = EMBED_COLOR
    icon_url = get_embed_icon_url()

    if icon_url and not getattr(embed.author, "name", None):
        embed.set_author(name="CFI", icon_url=icon_url)

    return embed


def make_embed(title, description, color=EMBED_COLOR):
    return brand_embed(discord.Embed(title=title, description=description, color=EMBED_COLOR))


def random_embed_color():
    return EMBED_COLOR


def clamp_embed_lines(lines, limit=1024, empty_text="None.", overflow_template="...and {remaining} more."):
    output = []
    total = 0

    for index, line in enumerate(lines):
        remaining = len(lines) - index
        overflow = overflow_template.format(remaining=remaining)
        candidate_length = total + len(line) + (1 if output else 0)

        if candidate_length + len(overflow) + 1 > limit:
            if output:
                output.append(overflow)
                return "\n".join(output)

            return overflow[:limit]

        output.append(line)
        total = candidate_length

    return "\n".join(output) if output else empty_text


async def send_private(interaction, embed):
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def safe_defer(interaction, ephemeral=False):
    if interaction.response.is_done():
        return True

    try:
        await interaction.response.defer(ephemeral=ephemeral)
        return True
    except discord.NotFound:
        return False
    except discord.HTTPException as error:
        if error.code == 40060:
            return True
        raise


async def require_command_role(interaction):
    if not isinstance(interaction.user, discord.Member):
        await send_private(
            interaction,
            make_embed(
                "Server Only",
                "This command can only be used inside a server.",
                ERROR_COLOR,
            ),
        )
        return False

    settings = load_settings()
    command_role_id = settings.get("tournament_organizer_role_id") or settings.get("command_role_id")
    command_role_id = int(command_role_id) if command_role_id else None

    if not command_role_id:
        if interaction.user.guild_permissions.manage_guild:
            return True

        await send_private(
            interaction,
            make_embed(
                "Organiser Role Not Set",
                "A server manager must run `/set_tournament_organizer_role` before this command can be used.",
                ERROR_COLOR,
            ),
        )
        return False

    configured_role = interaction.guild.get_role(command_role_id) if interaction.guild else None

    if not configured_role:
        if interaction.user.guild_permissions.manage_guild:
            return True

        await send_private(
            interaction,
            make_embed(
                "Organiser Role Missing",
                "The saved organiser role no longer exists. A server manager must run `/set_tournament_organizer_role` again.",
                ERROR_COLOR,
            ),
        )
        return False

    if any(role.id == command_role_id for role in interaction.user.roles):
        return True

    if interaction.guild and interaction.guild.owner_id == interaction.user.id:
        return True

    await send_private(
        interaction,
        make_embed(
            "Missing Role",
            f"You need the tournament organiser role {configured_role.mention} to use this command.",
            ERROR_COLOR,
        ),
    )
    return False


def has_command_role_access(interaction):
    if not isinstance(interaction.user, discord.Member):
        return False

    if interaction.guild and interaction.guild.owner_id == interaction.user.id:
        return True

    settings = load_settings()
    command_role_id = settings.get("tournament_organizer_role_id") or settings.get("command_role_id")
    command_role_id = int(command_role_id) if command_role_id else None

    if not command_role_id:
        return bool(interaction.user.guild_permissions.manage_guild)

    return any(role.id == command_role_id for role in interaction.user.roles)


def make_leaderboard_embed(scores, summary=None):
    embed = brand_embed(discord.Embed(
        title=LEADERBOARD_NAME,
        description=summary,
        color=EMBED_COLOR,
    ))

    if not scores:
        embed.description = summary or "No scores have been added yet."
        return embed

    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    for index, (player_id, score) in enumerate(sorted_scores[:10], start=1):
        rank_icon = RANK_MEDALS.get(index, RANK_SPACER)
        rank = f"{rank_icon} #{index}"
        player_label = f"<@{player_id}>" if str(player_id).isdigit() else player_id

        embed.add_field(
            name=f"{rank} {player_label}",
            value=f"Prestige: **{score}**",
            inline=False,
        )

    embed.set_footer(text=f"Showing top {min(len(sorted_scores), 10)} of {len(sorted_scores)} players")
    return embed


def add_prestige_to_member(member, prestige_score):
    member_id = str(member.id)
    scores = load_scores()
    record_undo("prestige score change", scores=scores)
    old_score = scores.get(member_id, 0)
    new_score = old_score + prestige_score
    scores[member_id] = new_score
    save_scores(scores)

    return scores, old_score, new_score


def make_statcard_embed(member, stats):
    scores = load_scores()
    prestige = scores.get(str(member.id), 0)
    embed = brand_embed(discord.Embed(
        title=f"\u26A1 {member.display_name}'s Stat Card",
        color=random_embed_color(),
    ))
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Prestige", value=f"**{prestige}**", inline=True)
    embed.add_field(name="Wins", value=f"**{stats['wins']}**", inline=True)
    embed.add_field(name="Losses", value=f"**{stats['losses']}**", inline=True)
    embed.add_field(name="Goals", value=f"**{stats['goals']}**", inline=True)
    embed.add_field(name="Event", value=str(stats.get("event", stats.get("even", 0))), inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Clan", value=stats["clan"], inline=False)
    return embed


def get_vote_result(player_one, player_two, votes_by_user):
    player_one_votes = sum(1 for voted_player_id in votes_by_user.values() if voted_player_id == player_one.id)
    player_two_votes = sum(1 for voted_player_id in votes_by_user.values() if voted_player_id == player_two.id)
    total_votes = len(votes_by_user)

    if total_votes:
        player_one_percent = player_one_votes / total_votes * 100
        player_two_percent = player_two_votes / total_votes * 100
    else:
        player_one_percent = 0
        player_two_percent = 0

    prestige_percent = max(player_one_percent, player_two_percent)
    prestige_score = round(prestige_percent * SCORE_PER_PERCENT)

    return {
        "player_one_votes": player_one_votes,
        "player_two_votes": player_two_votes,
        "total_votes": total_votes,
        "player_one_percent": player_one_percent,
        "player_two_percent": player_two_percent,
        "prestige_percent": prestige_percent,
        "prestige_score": prestige_score,
    }


def make_vote_embed(player_one, player_two, votes_by_user, closed=False, match_id=None, confirmed=False):
    result = get_vote_result(player_one, player_two, votes_by_user)
    title = "Match Vote Closed" if closed else "Match Vote Started"
    description = (
        f"{player_one.mention} vs {player_two.mention}\n\n"
        "Vote for who you think will win this match."
    )

    embed = discord.Embed(title=title, description=description, color=EMBED_COLOR)
    embed.add_field(
        name=player_one.display_name,
        value=f"Votes: **{result['player_one_votes']}** ({result['player_one_percent']:.1f}%)",
        inline=True,
    )
    embed.add_field(
        name=player_two.display_name,
        value=f"Votes: **{result['player_two_votes']}** ({result['player_two_percent']:.1f}%)",
        inline=True,
    )

    if closed:
        embed.add_field(
            name="Prestige Pool",
            value=(
                f"Current percent: **{result['prestige_percent']:.1f}%**\n"
                f"Prestige score: **{result['prestige_score']}**\n"
                "This pool goes toward the winner of the match."
            ),
            inline=False,
        )

        if confirmed:
            embed.add_field(name="Status", value="Winner confirmed.", inline=False)
    else:
        embed.add_field(
            name="Voting Closes",
            value="Automatically closes after **6 minutes**.",
            inline=False,
        )

    footer = f"Total votes: {result['total_votes']}"
    if match_id is not None:
        footer = f"Match ID: {match_id} | {footer}"
    embed.set_footer(text=footer)
    return embed


def add_vote_prestige_to_winner(vote, winner):
    result = get_vote_result(vote.player_one, vote.player_two, vote.votes_by_user)
    prestige_score = result["prestige_score"]
    scores, old_score, new_score = add_prestige_to_member(winner, prestige_score)

    return scores, old_score, new_score, prestige_score


def pair_key(player_one_id, player_two_id):
    return "-".join(sorted([str(player_one_id), str(player_two_id)]))


def find_round_robin_pairings(player_ids, played_pairs):
    played_pair_set = set(played_pairs)

    def search(remaining_ids, current_pairs):
        if not remaining_ids:
            return current_pairs

        first_id = remaining_ids[0]
        possible_opponents = remaining_ids[1:]
        random.shuffle(possible_opponents)

        for opponent_id in possible_opponents:
            current_pair_key = pair_key(first_id, opponent_id)

            if current_pair_key in played_pair_set:
                continue

            next_remaining = [
                player_id for player_id in remaining_ids
                if player_id not in (first_id, opponent_id)
            ]
            result = search(next_remaining, current_pairs + [(first_id, opponent_id)])

            if result:
                return result

        return None

    shuffled_ids = list(player_ids)

    for _ in range(300):
        random.shuffle(shuffled_ids)
        result = search(shuffled_ids, [])

        if result:
            return result

    return None


def make_matchups_embed(round_number, pairings):
    embed = discord.Embed(
        title=f"CFI Endgame Matchups - Round {round_number}",
        color=EMBED_COLOR,
    )

    for index, (player_one_id, player_two_id) in enumerate(pairings, start=1):
        embed.add_field(
            name=f"Match {index}",
            value=f"<@{player_one_id}> vs <@{player_two_id}>",
            inline=False,
        )

    embed.set_footer(text="Pairings avoid previous opponents where possible.")
    return embed


def get_guild_key(guild):
    return str(guild.id) if guild else None


def tournament_belongs_to_guild(tournament, guild):
    if not guild:
        return True

    guild_key = str(guild.id)
    saved_guild_id = tournament.get("guild_id")

    if saved_guild_id:
        return str(saved_guild_id) == guild_key

    for channel_id in tournament.get("channels", {}).values():
        if not str(channel_id).isdigit():
            continue

        channel_id = int(channel_id)
        channel = guild.get_channel_or_thread(channel_id) if hasattr(guild, "get_channel_or_thread") else guild.get_channel(channel_id)

        if channel:
            tournament["guild_id"] = guild_key
            return True

    return False


def set_active_tournament(tournaments, guild, tournament_id):
    guild_key = get_guild_key(guild)

    if guild_key:
        tournaments.setdefault("active_by_guild", {})[guild_key] = str(tournament_id) if tournament_id else None
    else:
        tournaments["active_id"] = str(tournament_id) if tournament_id else None


def get_active_tournament(tournaments, guild=None):
    guild_key = get_guild_key(guild)
    active_id = None

    if guild_key:
        active_id = tournaments.get("active_by_guild", {}).get(guild_key)

    if active_id is None and not guild_key:
        active_id = tournaments.get("active_id")

    if active_id is None and guild_key:
        legacy_id = tournaments.get("active_id")
        legacy_tournament = tournaments.get("tournaments", {}).get(str(legacy_id)) if legacy_id is not None else None

        if legacy_tournament and tournament_belongs_to_guild(legacy_tournament, guild):
            active_id = legacy_id
            set_active_tournament(tournaments, guild, legacy_id)

    if active_id is None:
        return None

    tournament = tournaments.get("tournaments", {}).get(str(active_id))

    if guild_key and tournament and not tournament_belongs_to_guild(tournament, guild):
        return None

    return tournament


def get_tournament_channel(guild, tournament, channel_key):
    if not guild:
        return None

    channel_id = tournament.get("channels", {}).get(channel_key)

    if not channel_id and channel_key == "round_control":
        channel_id = tournament.get("channels", {}).get("inscriptions")

    if not channel_id:
        return None

    if not str(channel_id).isdigit():
        return None

    channel_id = int(channel_id)

    if hasattr(guild, "get_channel_or_thread"):
        return guild.get_channel_or_thread(channel_id)

    return guild.get_channel(channel_id)


def is_tournament_post_channel(channel):
    return isinstance(channel, (discord.TextChannel, discord.Thread))


def invalid_tournament_channel_embed(channel):
    return make_embed(
        "Invalid Channel",
        (
            f"{channel.mention if hasattr(channel, 'mention') else channel} cannot receive normal bot messages.\n"
            "Choose a normal text channel, announcement channel, or a specific forum post/thread."
        ),
        ERROR_COLOR,
    )


async def send_tournament_update(interaction, tournament, channel_key, embed):
    channel = get_tournament_channel(interaction.guild, tournament, channel_key)

    if not channel:
        await interaction.followup.send(embed=embed)
        return

    if channel.id == interaction.channel_id:
        await interaction.followup.send(embed=embed)
        return

    await channel.send(embed=embed)
    await interaction.followup.send(
        embed=make_embed("Posted", f"Posted in {channel.mention}.", SUCCESS_COLOR),
        ephemeral=True,
    )


async def send_tournament_channel_embed(guild, tournament, channel_key, embed):
    channel = get_tournament_channel(guild, tournament, channel_key)

    if not channel:
        return False

    await channel.send(embed=embed)
    return True


async def upsert_tournament_control_center(guild, tournament):
    channel = get_tournament_channel(guild, tournament, "inscriptions")

    if not channel:
        return False

    is_setup = tournament.get("status") == "setup"
    embeds = make_tournament_embeds(tournament, guild) if is_setup else make_round_control_embeds(tournament, guild)
    embed = embeds[0]
    view = TournamentHubView(tournament["id"]) if is_setup else None
    messages = tournament.setdefault("messages", {})
    message_id = messages.get("control_center")

    if message_id:
        try:
            message = await channel.fetch_message(int(message_id))
            await message.edit(embed=embed, view=view)
            if is_setup:
                await sync_control_center_extra_embeds(channel, messages, embeds[1:])
                await sync_round_control_extra_embeds(channel, messages, [])
            if not is_setup:
                await sync_control_center_extra_embeds(channel, messages, [])
                messages["round_control"] = str(message.id)
                await sync_round_control_extra_embeds(channel, messages, embeds[1:])
            return False
        except (discord.NotFound, discord.Forbidden, discord.HTTPException, ValueError):
            pass

    message = await channel.send(embed=embed, view=view)
    messages["control_center"] = str(message.id)
    if is_setup:
        await sync_control_center_extra_embeds(channel, messages, embeds[1:])
        await sync_round_control_extra_embeds(channel, messages, [])
    if not is_setup:
        await sync_control_center_extra_embeds(channel, messages, [])
        messages["round_control"] = str(message.id)
        await sync_round_control_extra_embeds(channel, messages, embeds[1:])
    return True


async def upsert_round_control_center(guild, tournament):
    if tournament.get("status") == "setup":
        return False

    channel = get_tournament_channel(guild, tournament, "round_control")

    if not channel:
        return False

    embeds = make_round_control_embeds(tournament, guild)
    embed = embeds[0]
    messages = tournament.setdefault("messages", {})
    inscriptions_channel = get_tournament_channel(guild, tournament, "inscriptions")
    control_center_id = messages.get("control_center")

    if inscriptions_channel and inscriptions_channel.id == channel.id and control_center_id:
        try:
            message = await channel.fetch_message(int(control_center_id))
            await message.edit(embed=embed, view=None)
            messages["round_control"] = str(message.id)
            await sync_round_control_extra_embeds(channel, messages, embeds[1:])
            return False
        except (discord.NotFound, discord.Forbidden, discord.HTTPException, ValueError):
            pass

    message_id = messages.get("round_control")

    if message_id:
        try:
            message = await channel.fetch_message(int(message_id))
            await message.edit(embed=embed)
            await sync_round_control_extra_embeds(channel, messages, embeds[1:])
            return False
        except (discord.NotFound, discord.Forbidden, discord.HTTPException, ValueError):
            pass

    message = await channel.send(embed=embed)
    messages["round_control"] = str(message.id)
    await sync_round_control_extra_embeds(channel, messages, embeds[1:])
    return True


async def sync_round_control_extra_embeds(channel, messages, extra_embeds):
    await sync_extra_embeds(channel, messages, "round_control_extra", extra_embeds)


async def sync_control_center_extra_embeds(channel, messages, extra_embeds):
    await sync_extra_embeds(channel, messages, "control_center_extra", extra_embeds)


async def sync_extra_embeds(channel, messages, key, extra_embeds):
    existing_ids = list(messages.get(key, []))
    next_ids = []

    for index, embed in enumerate(extra_embeds):
        message = None

        if index < len(existing_ids):
            try:
                message = await channel.fetch_message(int(existing_ids[index]))
                await message.edit(embed=embed, view=None)
            except (discord.NotFound, discord.Forbidden, discord.HTTPException, ValueError):
                message = None

        if message is None:
            message = await channel.send(embed=embed)

        next_ids.append(str(message.id))

    for stale_id in existing_ids[len(extra_embeds):]:
        try:
            stale_message = await channel.fetch_message(int(stale_id))
            await stale_message.delete()
        except (discord.NotFound, discord.Forbidden, discord.HTTPException, ValueError):
            pass

    if next_ids:
        messages[key] = next_ids
    else:
        messages.pop(key, None)


def tournament_player_label(player, guild=None, prefer_mention=False):
    if not player:
        return "BYE"

    player_id = str(player.get("id", ""))
    player_name = str(player.get("name", "")).strip()

    if guild and player_id.isdigit():
        member = guild.get_member(int(player_id))

        if member:
            return member.mention if prefer_mention else member.display_name

    if player_name:
        return player_name

    if player_id.isdigit():
        return f"<@{player_id}>" if prefer_mention else "Unknown player"

    return player_id or "Unknown player"


def get_default_profile():
    return {
        "prestige": 0,
        "wins": 0,
        "losses": 0,
        "goals_for": 0,
        "goals_against": 0,
        "last_lost_to": "",
        "last_lost_to_name": "",
        "finishes": {},
        "clan": "None",
        "country": "",
        "country_code": "",
        "url": "",
        "player_grade_seed_gd": 0.0,
        "player_grade_seed_matches": 0,
    }


def get_profile(profiles, player_id):
    profile = profiles.setdefault(str(player_id), get_default_profile())
    profile.setdefault("prestige", 0)
    profile.setdefault("wins", 0)
    profile.setdefault("losses", 0)
    profile.setdefault("goals_for", 0)
    profile.setdefault("goals_against", 0)
    profile.setdefault("last_lost_to", "")
    profile.setdefault("last_lost_to_name", "")
    profile.setdefault("finishes", {})
    profile.setdefault("clan", "None")
    profile.setdefault("country", "")
    profile.setdefault("country_code", "")
    profile.setdefault("url", "")
    profile.setdefault("player_grade_seed_gd", 0.0)
    profile.setdefault("player_grade_seed_matches", 0)
    return profile


def country_flag(country_code):
    country_code = str(country_code or "").upper()

    if len(country_code) != 2 or not country_code.isalpha():
        return ""

    return "".join(chr(0x1F1E6 + ord(letter) - ord("A")) for letter in country_code)


def normalize_country(country):
    clean_country = str(country or "").strip()

    if not clean_country or clean_country.lower() in {"none", "clear", "remove"}:
        return "", ""

    upper_country = clean_country.upper()

    if len(upper_country) == 2 and upper_country.isalpha():
        for country_name, country_code in COUNTRIES.items():
            if country_code == upper_country:
                return country_name, country_code

    alias = COUNTRY_ALIASES.get(clean_country.lower())

    if alias:
        return alias, COUNTRIES.get(alias, "")

    for country_name, country_code in COUNTRIES.items():
        if country_name.lower() == clean_country.lower():
            return country_name, country_code

    return None, None


def get_tournament_finish_label(tournament, round_number, champion=False):
    if champion:
        return "Champion"

    bracket_size = next_power_of_two(max(1, len(tournament.get("players", []))))
    remaining_size = max(2, bracket_size // (2 ** max(0, int(round_number or 1) - 1)))
    return f"{remaining_size}'s"


def add_profile_finish(profile, finish_label):
    finishes = profile.setdefault("finishes", {})
    finishes[finish_label] = finishes.get(finish_label, 0) + 1


def get_profile_average_gd(profile):
    matches_played = int(profile.get("wins", 0) or 0) + int(profile.get("losses", 0) or 0)
    seed_matches = max(0, int(profile.get("player_grade_seed_matches", 0) or 0))
    seed_gd = float(profile.get("player_grade_seed_gd", 0.0) or 0.0)
    total_matches = matches_played + seed_matches

    if total_matches <= 0:
        return 0.0

    goals_for = int(profile.get("goals_for", 0) or 0)
    goals_against = int(profile.get("goals_against", 0) or 0)
    match_gd_total = goals_for - goals_against
    seeded_gd_total = seed_gd * seed_matches
    return (seeded_gd_total + match_gd_total) / total_matches


PLAYER_GRADE_TIERS = [
    ("legendary", "Legendary", 2.5, "\U0001F308"),
    ("generational", "Generational", 1.75, "\U0001F7E3"),
    ("world_class", "World Class", 1.0, "\U0001F535"),
    ("trash", "Trash", float("-inf"), "\U0001F5D1\uFE0F"),
]


def get_profile_player_grade(profile):
    average_gd = get_profile_average_gd(profile)

    for key, name, minimum_gd, emoji in PLAYER_GRADE_TIERS:
        if average_gd >= minimum_gd:
            return key, f"{emoji} {name}", average_gd

    return "trash", "\U0001F5D1\uFE0F Trash", average_gd


def apply_match_profile_rewards(tournament, match):
    if match.get("profile_rewards"):
        return match["profile_rewards"]

    winner = match.get("winner")
    player_one = match.get("player_one")
    player_two = match.get("player_two")

    if not winner or not player_one or not player_two:
        return None

    loser = player_two if str(winner["id"]) == str(player_one["id"]) else player_one
    score = match.get("score", {})
    player_one_goals = int(score.get("player_one", 0) or 0)
    player_two_goals = int(score.get("player_two", 0) or 0)
    winner_is_player_one = str(winner["id"]) == str(player_one["id"])
    winner_goals = player_one_goals if winner_is_player_one else player_two_goals
    loser_goals = player_two_goals if winner_is_player_one else player_one_goals
    winner_bonus = sum(random.randint(2000, 2500) for _ in range(max(0, int(winner_goals or 0))))
    winner_gain = 50000 + winner_bonus
    loser_gain = 25000
    profiles = load_profiles()
    winner_profile = get_profile(profiles, winner["id"])
    loser_profile = get_profile(profiles, loser["id"])
    winner_profile["prestige"] += winner_gain
    winner_profile["wins"] += 1
    winner_profile["goals_for"] += winner_goals
    winner_profile["goals_against"] += loser_goals
    loser_profile["prestige"] += loser_gain
    loser_profile["losses"] += 1
    loser_profile["goals_for"] += loser_goals
    loser_profile["goals_against"] += winner_goals
    loser_profile["last_lost_to"] = str(winner["id"])
    loser_profile["last_lost_to_name"] = str(winner.get("name", "Unknown"))

    round_number = int(match.get("round", 1) or 1)
    add_profile_finish(loser_profile, get_tournament_finish_label(tournament, round_number))

    bracket_size = next_power_of_two(max(1, len(tournament.get("players", []))))
    final_round = max(1, bracket_size.bit_length() - 1)

    if round_number >= final_round:
        add_profile_finish(winner_profile, get_tournament_finish_label(tournament, round_number, champion=True))

    rewards = {
        "winner_id": str(winner["id"]),
        "loser_id": str(loser["id"]),
        "winner_gain": winner_gain,
        "winner_bonus": winner_bonus,
        "winner_goals": winner_goals,
        "loser_gain": loser_gain,
        "loser_goals": loser_goals,
    }
    match["profile_rewards"] = rewards
    save_profiles(profiles)
    return rewards


def make_profile_embed(member, profile):
    finishes = profile.get("finishes", {})
    profile_url = str(profile.get("url", "")).strip()
    embed = brand_embed(discord.Embed(
        title=f"\u26A1 {member.display_name}'s Profile \u26A1",
        description="Tournament identity and all-time record",
        url=profile_url if profile_url else None,
        color=random_embed_color(),
    ))
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="\U0001F3C6 Prestige Points", value=f"{profile.get('prestige', 0):,}", inline=True)
    wins = profile.get("wins", 0)
    losses = profile.get("losses", 0)
    embed.add_field(name="\u2694\uFE0F Win-Loss Record", value=f"{wins}-{losses}", inline=True)

    last_lost_to = str(profile.get("last_lost_to", "")).strip()

    if last_lost_to.isdigit():
        arch_nemesis = f"<@{last_lost_to}>"
    else:
        arch_nemesis = str(profile.get("last_lost_to_name", "")).strip() or "None yet"

    embed.add_field(name="\U0001F3AF Arch Nemesis", value=arch_nemesis, inline=True)
    embed.add_field(name="\U0001F6E1\uFE0F Clan", value=profile.get("clan", "None"), inline=True)

    if profile.get("country"):
        flag = country_flag(profile.get("country_code"))
        embed.add_field(name="\U0001F30D Country", value=f"{flag} {profile['country']}", inline=True)

    if profile_url:
        embed.set_image(url=profile_url)

    finish_order = {"Champion": 0}

    def finish_sort_key(item):
        label, _count = item
        if label in finish_order:
            return (finish_order[label], 0)
        number = int(str(label).replace("'s", "")) if str(label).replace("'s", "").isdigit() else 999999
        return (1, number)

    if finishes:
        finish_lines = [
            f"{label}: {count}"
            for label, count in sorted(finishes.items(), key=finish_sort_key)
        ]
        finish_text = "\n".join(finish_lines)
    else:
        finish_text = "No tournament finishes yet."

    embed.add_field(name="\U0001F31F Highest Finishes", value=finish_text[:1024], inline=False)
    return embed

async def get_tournament_member(guild, player):
    if not player or not str(player.get("id", "")).isdigit():
        return None

    player_id = int(player["id"])
    member = guild.get_member(player_id)

    if member:
        return member

    try:
        return await guild.fetch_member(player_id)
    except discord.HTTPException:
        return None


async def post_updated_match_profiles(guild, tournament, match):
    channel = get_tournament_channel(guild, tournament, "profiles")

    if not channel:
        return False

    player_ids = []

    for player in (match.get("winner"), match.get("player_one"), match.get("player_two")):
        if player and str(player.get("id")) not in player_ids:
            player_ids.append(str(player["id"]))

    profiles = load_profiles()
    posted = False

    for player_id in player_ids:
        player = next(
            (
                candidate
                for candidate in (match.get("winner"), match.get("player_one"), match.get("player_two"))
                if candidate and str(candidate.get("id")) == player_id
            ),
            None,
        )
        member = await get_tournament_member(guild, player)

        if not member:
            continue

        await channel.send(embed=make_profile_embed(member, get_profile(profiles, member.id)))
        posted = True

    return posted


def tournament_member_entry(member):
    return {
        "id": str(member.id),
        "name": member.display_name,
    }


def add_member_to_tournament(tournament, member):
    if tournament.get("status") != "setup":
        return False, "started"

    player_id = str(member.id)

    if any(existing_player["id"] == player_id for existing_player in tournament["players"]):
        return False, "exists"

    tournament["players"].append(tournament_member_entry(member))
    return True, "added"


def next_power_of_two(number):
    power = 1

    while power < number:
        power *= 2

    return power


def challonge_seed_order(size):
    if size <= 1:
        return [1]

    order = [1, 2]

    while len(order) < size:
        next_size = len(order) * 2
        order = [seed for existing_seed in order for seed in (existing_seed, next_size + 1 - existing_seed)]

    return order


def arrange_players_for_challonge_seed_order(players):
    target_size = next_power_of_two(len(players))
    seed_order = challonge_seed_order(target_size)
    return [
        players[seed - 1] if seed <= len(players) else None
        for seed in seed_order
    ]


def make_tournament_match(round_number, match_number, player_one, player_two):
    return {
        "id": f"R{round_number}M{match_number}",
        "round": round_number,
        "player_one": player_one,
        "player_two": player_two,
        "winner": None,
        "state": "open",
    }


def create_tournament_round(players, round_number):
    matches = []

    for index in range(0, len(players), 2):
        match_number = len(matches) + 1
        player_one = players[index]
        player_two = players[index + 1] if index + 1 < len(players) else None
        match = make_tournament_match(round_number, match_number, player_one, player_two)

        if player_one and not player_two:
            match["winner"] = player_one
            match["state"] = "completed"
        elif player_two and not player_one:
            match["winner"] = player_two
            match["state"] = "completed"

        matches.append(match)

    return matches


def start_tournament_bracket(tournament, shuffle_players=False):
    players = list(tournament["players"])

    if shuffle_players:
        random.shuffle(players)

    players = arrange_players_for_challonge_seed_order(players)

    tournament["status"] = "running"
    tournament["current_round"] = 1
    tournament["rounds"] = [create_tournament_round(players, 1)]
    tournament["winner"] = None
    advance_tournament_byes(tournament)


def advance_tournament_byes(tournament):
    while tournament.get("status") == "running":
        current_round = tournament["rounds"][-1]

        if any(match["state"] != "completed" for match in current_round):
            return

        winners = [match["winner"] for match in current_round if match.get("winner")]

        if len(winners) == 1:
            tournament["status"] = "completed"
            tournament["winner"] = winners[0]
            return

        next_round_number = len(tournament["rounds"]) + 1
        tournament["rounds"].append(create_tournament_round(winners, next_round_number))
        tournament["current_round"] = next_round_number


def find_tournament_match(tournament, match_id):
    searched_id = str(match_id).upper()
    current_round = tournament.get("current_round", 1)

    if searched_id.isdigit():
        searched_id = f"R{current_round}M{searched_id}"

    for round_matches in tournament.get("rounds", []):
        for match in round_matches:
            if str(match.get("id", "")).upper() == searched_id:
                return match

    return None


def find_open_tournament_match_by_players(tournament, player_one_id, player_two_id):
    searched_ids = {str(player_one_id), str(player_two_id)}

    for round_matches in tournament.get("rounds", []):
        for match in round_matches:
            if match.get("state") not in ("open", "draw"):
                continue

            match_ids = {
                str(player["id"])
                for player in [match.get("player_one"), match.get("player_two")]
                if player
            }

            if match_ids == searched_ids:
                return match

    return None


def find_open_tournament_match_by_player(tournament, player_id):
    searched_id = str(player_id)

    for round_matches in tournament.get("rounds", []):
        for match in round_matches:
            if match.get("state") not in ("open", "draw"):
                continue

            match_ids = {
                str(player["id"])
                for player in [match.get("player_one"), match.get("player_two")]
                if player
            }

            if searched_id in match_ids:
                return match

    return None


def find_any_tournament_match_by_player(tournament, player_id):
    searched_id = str(player_id)

    for round_matches in tournament.get("rounds", []):
        for match in round_matches:
            match_ids = {
                str(player["id"])
                for player in [match.get("player_one"), match.get("player_two")]
                if player
            }

            if searched_id in match_ids:
                return match

    return None


def tournament_matches_by_id(tournament):
    matches = {}

    for round_matches in tournament.get("rounds", []):
        for match in round_matches:
            match_id = str(match.get("id", ""))

            if match_id:
                matches[match_id] = match

    return matches


def find_matches_reopened_by_undo(current_tournament, restored_tournament):
    current_matches = tournament_matches_by_id(current_tournament or {})
    restored_matches = tournament_matches_by_id(restored_tournament or {})
    reopened = []

    for match_id, current_match in current_matches.items():
        restored_match = restored_matches.get(match_id)

        if not restored_match:
            continue

        if current_match.get("state") == "completed" and restored_match.get("state") != "completed":
            if current_match.get("player_one") and current_match.get("player_two"):
                reopened.append(current_match)

    return reopened


def get_current_round_matches(tournament):
    current_round = int(tournament.get("current_round", 1) or 1)

    for round_matches in tournament.get("rounds", []):
        if round_matches and int(round_matches[0].get("round", 0) or 0) == current_round:
            return round_matches

    return tournament.get("rounds", [])[-1] if tournament.get("rounds") else []


async def dm_next_round_opponents(guild, tournament):
    current_round = int(tournament.get("current_round", 1) or 1)
    sent_count = 0
    failed_count = 0

    if tournament.get("status") != "running":
        return sent_count, failed_count

    if tournament.get("test_mode"):
        return sent_count, failed_count

    for match in get_current_round_matches(tournament):
        if match.get("state") != "open":
            continue

        player_one = match.get("player_one")
        player_two = match.get("player_two")

        if not player_one or not player_two:
            continue

        pairings = (
            (player_one, player_two),
            (player_two, player_one),
        )

        for player, opponent in pairings:
            member = guild.get_member(int(player["id"])) if str(player.get("id", "")).isdigit() else None

            if not member:
                failed_count += 1
                continue

            embed = make_embed(
                f"{tournament['name']} - Round {current_round}",
                (
                    "Your next opponent is ready.\n\n"
                    f"**Opponent:** {tournament_player_label(opponent, guild)}\n"
                    f"**Round:** {current_round}\n\n"
                    "Play your match and report the score with `/score`."
                ),
                random_embed_color(),
            )

            try:
                await member.send(
                    content=f"{member.mention} your next tournament opponent is ready.",
                    embed=embed,
                    allowed_mentions=discord.AllowedMentions(users=True, roles=False, everyone=False),
                )
                sent_count += 1
            except discord.HTTPException:
                failed_count += 1

    return sent_count, failed_count


def make_progress_bar(completed, total, width=10):
    empty_block = "\u2B1B"

    if total <= 0:
        return empty_block * width

    filled = round((completed / total) * width)
    fill_block = "\U0001F7E9" if completed >= total else "\U0001F7EA"
    return fill_block * filled + empty_block * (width - filled)


def chunk_embed_lines(lines, limit=1024):
    chunks = []
    current = []
    current_length = 0

    for line in lines:
        line = str(line)
        separator_length = 1 if current else 0

        if current and current_length + separator_length + len(line) > limit:
            chunks.append("\n".join(current))
            current = []
            current_length = 0

        if len(line) > limit:
            chunks.append(line[:limit])
            continue

        current.append(line)
        current_length += len(line) + (1 if len(current) > 1 else 0)

    if current:
        chunks.append("\n".join(current))

    return chunks


def add_chunked_fields_to_embeds(embeds, continuation_title, name, lines, empty_text):
    chunks = chunk_embed_lines(lines) if lines else [empty_text]

    for index, chunk in enumerate(chunks):
        current = embeds[-1]
        field_name = name if index == 0 else f"{name} - continued"
        current_size = len(current.title or "") + len(current.description or "")
        current_size += sum(len(field.name) + len(field.value) for field in current.fields)

        if len(current.fields) >= 5 or current_size + len(field_name) + len(chunk) > 5500:
            current = brand_embed(discord.Embed(
                title=f"\u2B50 {continuation_title} \u2B50",
                color=random_embed_color(),
            ))
            embeds.append(current)

        current.add_field(name=field_name, value=chunk, inline=False)


def add_chunked_round_field(embeds, base_title, name, lines, empty_text):
    add_chunked_fields_to_embeds(embeds, f"{base_title} - continued", name, lines, empty_text)


def make_round_control_embeds(tournament, guild=None, advanced=False):
    current_round = int(tournament.get("current_round", 1) or 1)
    round_matches = get_current_round_matches(tournament)
    total_matches = len(round_matches)
    completed_matches = sum(1 for match in round_matches if match.get("state") == "completed")
    progress_percent = round((completed_matches / total_matches) * 100) if total_matches else 0
    title = "Next Round Started" if advanced else "Round Control"

    if tournament.get("status") == "completed":
        title = "Tournament Completed"

    embeds = [brand_embed(discord.Embed(
        title=f"\u2B50 {title} \u2B50",
        description=(
            f"**{tournament['name']}**\n"
            f"Round **{current_round}** overview"
            + ("\n\U0001F9EA **TEST MODE:** profile rewards are disabled." if tournament.get("test_mode") else "")
        ),
        color=random_embed_color(),
    ))]
    embed = embeds[0]

    if tournament.get("challonge_url"):
        embed.add_field(name="Challonge", value=f"[Open Bracket]({tournament['challonge_url']})", inline=False)

    embed.add_field(
        name="Advancement",
        value=f"`{make_progress_bar(completed_matches, total_matches)}` **{progress_percent}%**\n{completed_matches}/{total_matches} matches completed",
        inline=False,
    )

    played_lines = []
    remaining_lines = []

    for match in round_matches:
        player_one = tournament_player_label(match.get("player_one"), guild)
        player_two = tournament_player_label(match.get("player_two"), guild)
        score = match.get("score")
        score_text = ""

        if isinstance(score, dict):
            score_text = f" **{score.get('player_one', 0)}-{score.get('player_two', 0)}**"

        if match.get("state") == "completed":
            winner = tournament_player_label(match.get("winner"), guild)
            dq_text = " | DQ" if match.get("dq") else ""
            played_lines.append(f"\u2705 {player_one} vs {player_two}{score_text} | Winner: {winner}{dq_text}")
        elif match.get("state") == "draw":
            remaining_lines.append(f"\U0001F91D {player_one} vs {player_two}{score_text} | Replay needed")
        else:
            remaining_lines.append(f"\u2694\uFE0F {player_one} vs {player_two}")

    add_chunked_round_field(embeds, title, "Played Matches", played_lines, "No matches completed yet.")
    add_chunked_round_field(embeds, title, "Still Needed", remaining_lines, "All matches are complete.")

    if tournament.get("winner"):
        embeds[-1].add_field(
            name="\U0001F3C6 Champion",
            value=f"\u2B50 {tournament_player_label(tournament['winner'], guild)} \u2B50",
            inline=False,
        )
    elif remaining_lines:
        embeds[-1].set_footer(text="Finish the remaining matches before using /next_round again.")
    else:
        embeds[-1].set_footer(text="Round is complete. Use /next_round to start the next round.")

    return embeds


def make_round_control_embed(tournament, guild=None, advanced=False):
    return make_round_control_embeds(tournament, guild, advanced)[0]


def make_participants_embed(tournament, guild=None):
    players = tournament.get("players", [])
    preview_count = 30
    preview_players = players[:preview_count]
    embed = brand_embed(discord.Embed(
        title=f"\u2B50 Participants - {tournament['name']} \u2B50",
        description=f"Registered players: **{len(players)}**",
        color=random_embed_color(),
    ))

    if tournament.get("start_time"):
        embed.add_field(name="Start Time", value=tournament["start_time"], inline=False)

    player_lines = [
        f"**{index}.** {tournament_player_label(player, guild)}"
        for index, player in enumerate(preview_players, start=1)
    ]

    if len(players) > preview_count:
        player_lines.append(f"...and {len(players) - preview_count} more registered players.")

    embed.add_field(
        name=f"Players Preview ({len(preview_players)}/{len(players)})",
        value="\n".join(player_lines) if player_lines else "No players registered yet.",
        inline=False,
    )
    embed.set_footer(text="Use /participants_export for the full list.")
    return embed

def load_result_font(size, bold=False, italic=False):
    if ImageFont is None:
        return None

    if bold and italic:
        font_names = ["arialbi.ttf", "segoeuiz.ttf", "segoeuib.ttf", "arialbd.ttf"]
    elif italic:
        font_names = ["ariali.ttf", "segoeuii.ttf", "arial.ttf", "segoeui.ttf"]
    elif bold:
        font_names = ["arialbd.ttf", "segoeuib.ttf"]
    else:
        font_names = ["arial.ttf", "segoeui.ttf"]

    for font_name in font_names:
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            continue

    return ImageFont.load_default()


def draw_centered_text(draw, box, text, font, fill, stroke_fill=None, stroke_width=0):
    left, top, right, bottom = box
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = left + ((right - left - text_width) / 2)
    y = top + ((bottom - top - text_height) / 2)
    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill,
        stroke_fill=stroke_fill,
        stroke_width=stroke_width,
    )


def draw_centered_shadow_text(draw, box, text, font, fill, shadow=(0, 0, 0, 125), offset=(3, 4)):
    left, top, right, bottom = box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = left + ((right - left - text_width) / 2)
    y = top + ((bottom - top - text_height) / 2)
    draw.text((x + offset[0], y + offset[1]), text, font=font, fill=shadow)
    draw.text((x, y), text, font=font, fill=fill)


def player_result_name(player):
    if not player:
        return "BYE"

    return str(player.get("name") or player.get("id") or "Player")[:28]


def fetch_media_bytes(url, max_bytes=10_000_000):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": CHALLONGE_USER_AGENT,
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        },
    )

    with urllib.request.urlopen(request, timeout=12) as response:
        data = response.read(max_bytes + 1)

    if len(data) > max_bytes:
        raise ValueError("media file is too large")

    return data


def fit_image(image, size):
    width, height = size
    image = image.convert("RGBA")
    image_width, image_height = image.size

    if image_width <= 0 or image_height <= 0:
        return Image.new("RGBA", size, (35, 0, 90, 255))

    scale = max(width / image_width, height / image_height)
    resized = image.resize((int(image_width * scale), int(image_height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - width) // 2)
    top = max(0, (resized.height - height) // 2)
    return resized.crop((left, top, left + width, top + height))


def make_default_result_background(size, frame_index=0, frame_count=1):
    width, height = size
    image = Image.new("RGBA", size, (88, 22, 210, 255))
    draw = ImageDraw.Draw(image)
    phase = frame_index / max(1, frame_count)

    for y in range(height):
        blend = y / max(1, height)
        color = (
            int(105 - 30 * blend),
            int(18 + 10 * blend),
            int(230 - 40 * blend),
            255,
        )
        draw.line((0, y, width, y), fill=color)

    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    offset = int(phase * width)
    glow_draw.ellipse((260 + offset % width - 360, 10, 700 + offset % width - 360, height + 180), fill=(180, 80, 255, 75))
    glow = glow.filter(ImageFilter.GaussianBlur(42))
    return Image.alpha_composite(image, glow)


def result_background_frames(media_url, size, frame_count=8):
    if not media_url:
        return []

    try:
        data = fetch_media_bytes(media_url)
        source = Image.open(io.BytesIO(data))
    except (OSError, ValueError, urllib.error.URLError, TimeoutError):
        return []

    total_frames = max(1, int(getattr(source, "n_frames", 1)))
    frames = []

    for index in range(min(frame_count, total_frames)):
        frame_number = int(index * total_frames / min(frame_count, total_frames))

        try:
            source.seek(frame_number)
            frame = source.copy()
        except EOFError:
            break

        frames.append(fit_image(frame, size))

    return frames


def player_avatar_image(guild, player, size):
    if not player:
        return Image.new("RGBA", (size, size), (20, 20, 28, 255))

    member = None
    player_id = player.get("id")

    try:
        member = guild.get_member(int(player_id)) if guild and player_id else None
    except (TypeError, ValueError):
        member = None

    if member:
        avatar_url = member.display_avatar.replace(size=256, static_format="png").url

        try:
            data = fetch_media_bytes(avatar_url, max_bytes=5_000_000)
            return fit_image(Image.open(io.BytesIO(data)), (size, size))
        except (OSError, ValueError, urllib.error.URLError, TimeoutError):
            pass

    image = Image.new("RGBA", (size, size), (24, 26, 42, 255))
    draw = ImageDraw.Draw(image)
    font = load_result_font(max(20, size // 4), bold=True)
    initial = player_result_name(player)[:1].upper() or "?"
    draw_centered_text(draw, (0, 0, size, size), initial, font, (255, 220, 90), stroke_fill=(0, 0, 0), stroke_width=2)
    return image


def draw_text_fit(draw, box, text, font_size, fill, stroke_fill=(0, 0, 0), stroke_width=2, bold=True):
    left, top, right, bottom = box
    text = str(text)

    for size in range(font_size, 13, -2):
        font = load_result_font(size, bold=bold)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)

        if bbox[2] - bbox[0] <= right - left - 12:
            draw_centered_text(draw, box, text, font, fill, stroke_fill=stroke_fill, stroke_width=stroke_width)
            return

    font = load_result_font(14, bold=bold)
    draw_centered_text(draw, box, text[:24], font, fill, stroke_fill=stroke_fill, stroke_width=stroke_width)


def draw_text_fit_shadow(draw, box, text, font_size, fill, shadow=(0, 0, 0, 190), offset=(3, 4), bold=True, italic=False):
    left, top, right, bottom = box
    text = str(text)

    for size in range(font_size, 13, -2):
        font = load_result_font(size, bold=bold, italic=italic)
        bbox = draw.textbbox((0, 0), text, font=font)

        if bbox[2] - bbox[0] <= right - left - 12:
            draw_centered_shadow_text(draw, box, text, font, fill, shadow=shadow, offset=offset)
            return

    font = load_result_font(14, bold=bold, italic=italic)
    draw_centered_shadow_text(draw, box, text[:24], font, fill, shadow=shadow, offset=offset)


def make_result_card_frame(guild, tournament, match, background, frame_index=0, frame_count=1):
    width, height = background.size
    image = background.convert("RGBA")
    draw = ImageDraw.Draw(image)

    score = match.get("score", {})
    player_one = match.get("player_one")
    player_two = match.get("player_two")
    player_one_name = player_result_name(player_one)
    player_two_name = player_result_name(player_two)
    player_one_score = int(score.get("player_one", 0) or 0)
    player_two_score = int(score.get("player_two", 0) or 0)
    winner_id = str(match.get("winner", {}).get("id", ""))
    left_winner = player_one and str(player_one.get("id")) == winner_id
    right_winner = player_two and str(player_two.get("id")) == winner_id
    rewards = match.get("profile_rewards") or {}
    loser_id = str(rewards.get("loser_id", ""))
    player_one_id = str(player_one.get("id", "")) if player_one else ""
    player_two_id = str(player_two.get("id", "")) if player_two else ""
    player_one_gain = 0
    player_two_gain = 0

    if player_one_id and player_one_id == winner_id:
        player_one_gain = int(rewards.get("winner_gain", 0) or 0)
    elif player_one_id and player_one_id == loser_id:
        player_one_gain = int(rewards.get("loser_gain", 0) or 0)

    if player_two_id and player_two_id == winner_id:
        player_two_gain = int(rewards.get("winner_gain", 0) or 0)
    elif player_two_id and player_two_id == loser_id:
        player_two_gain = int(rewards.get("loser_gain", 0) or 0)

    top_font = load_result_font(50, bold=True, italic=True)
    small_font = load_result_font(22, bold=True, italic=True)
    score_font = load_result_font(156, bold=True, italic=True)
    dash_font = load_result_font(134, bold=True, italic=True)

    draw_centered_shadow_text(
        draw,
        (0, 8, width, 70),
        "CFI",
        top_font,
        (255, 255, 255),
        shadow=(0, 0, 0, 135),
        offset=(3, 4),
    )
    draw_centered_shadow_text(
        draw,
        (0, 62, width, 96),
        f"{tournament.get('name', 'Tournament')} | Round {match.get('round')}",
        small_font,
        (255, 255, 255),
        shadow=(0, 0, 0, 115),
        offset=(2, 3),
    )

    avatar_size = 184
    left_avatar_box = (28, 102)
    right_avatar_box = (width - 28 - avatar_size, 102)
    left_border = (255, 215, 50) if left_winner else (90, 210, 255)
    right_border = (255, 215, 50) if right_winner else (90, 210, 255)

    for box, border in ((left_avatar_box, left_border), (right_avatar_box, right_border)):
        x, y = box
        draw.rectangle((x - 5, y - 5, x + avatar_size + 5, y + avatar_size + 42), fill=(5, 5, 10, 210), outline=border, width=4)

    left_avatar = player_avatar_image(guild, player_one, avatar_size)
    right_avatar = player_avatar_image(guild, player_two, avatar_size)
    image.alpha_composite(left_avatar, left_avatar_box)
    image.alpha_composite(right_avatar, right_avatar_box)
    draw = ImageDraw.Draw(image)

    name_bar_height = 38
    draw.rectangle((28, 102 + avatar_size, 28 + avatar_size, 102 + avatar_size + name_bar_height), fill=(0, 0, 0, 230))
    draw.rectangle((right_avatar_box[0], 102 + avatar_size, right_avatar_box[0] + avatar_size, 102 + avatar_size + name_bar_height), fill=(0, 0, 0, 230))
    draw_text_fit_shadow(draw, (28, 102 + avatar_size, 28 + avatar_size, 102 + avatar_size + name_bar_height), player_one_name, 27, (255, 255, 255), offset=(2, 2), italic=True)
    draw_text_fit_shadow(draw, (right_avatar_box[0], 102 + avatar_size, right_avatar_box[0] + avatar_size, 102 + avatar_size + name_bar_height), player_two_name, 27, (255, 255, 255), offset=(2, 2), italic=True)

    prestige_bar_top = 102 + avatar_size + name_bar_height + 8
    empty_gain_text = "Test mode" if tournament.get("test_mode") else "Prestige pending"
    left_gain_text = f"+{player_one_gain:,} PP" if player_one_gain else empty_gain_text
    right_gain_text = f"+{player_two_gain:,} PP" if player_two_gain else empty_gain_text
    prestige_color = (220, 250, 255)
    draw_text_fit_shadow(draw, (32, prestige_bar_top, 24 + avatar_size, prestige_bar_top + 34), left_gain_text, 20, prestige_color, offset=(2, 2), italic=True)
    draw_text_fit_shadow(draw, (right_avatar_box[0] + 4, prestige_bar_top, right_avatar_box[0] + avatar_size - 4, prestige_bar_top + 34), right_gain_text, 20, prestige_color, offset=(2, 2), italic=True)

    draw_centered_shadow_text(draw, (222, 94, 738, 316), f"{player_one_score} - {player_two_score}", score_font, (255, 255, 255), shadow=(0, 0, 0, 145), offset=(5, 6))
    draw_centered_shadow_text(draw, (392, 122, 568, 264), "-", dash_font, (255, 255, 255), shadow=(0, 0, 0, 145), offset=(5, 6))

    if match.get("dq") or tournament.get("test_mode"):
        footer = "DQ" if match.get("dq") else "TEST MODE"
        draw_text_fit_shadow(draw, (392, 326, width - 392, 364), footer, 22, (255, 255, 255), offset=(2, 2), italic=True)
    return image.convert("P", palette=Image.Palette.ADAPTIVE)


def make_result_card_file(guild, tournament, match):
    if Image is None:
        return None

    media_url = get_result_media_url()

    if not media_url:
        return None

    size = (960, 420)
    backgrounds = result_background_frames(media_url, size, frame_count=8)

    if not backgrounds:
        backgrounds = [make_default_result_background(size, index, 8) for index in range(8)]

    frames = [
        make_result_card_frame(guild, tournament, match, background, index, len(backgrounds))
        for index, background in enumerate(backgrounds)
    ]
    buffer = io.BytesIO()
    filename = f"result_{match.get('id', 'match')}.gif"
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=130,
        loop=0,
        optimize=False,
    )
    buffer.seek(0)
    return discord.File(buffer, filename=filename), filename


def get_result_media_url():
    settings = load_settings()
    return str(settings.get("result_media_url", "")).strip()


LOSER_QUOTES = [
    ("Jinpachi Ego", "Luck descends equally upon only those who are truly prepared to fight."),
    ("Jinpachi Ego", "To be the best striker in the world, you have to be the most selfish person in the world."),
    ("Jinpachi Ego", "The only ones who will survive are the ones who can adapt."),
    ("Jinpachi Ego", "Impossible? What kind of a concept is that? Who decided it was impossible?"),
    ("Yoichi Isagi", "I'm not on this field to make friends. I'm here to devour everyone."),
    ("Yoichi Isagi", "Shut up, genius. I'm feeling incredible right now."),
    ("Yoichi Isagi", "No matter how much you knock on the door to someone's heart, you can't change them, so it's always you who has to change."),
    ("Shoei Barou", "Entrusting the goal to them might indeed salvage me from this sense of defeat, but that's just escapism for those with broken dreams... I refuse to live in a future like that."),
    ("Shoei Barou", "Get out of my way, you are just an obstacle."),
    ("Rin Itoshi", "Are you just a parasite feeding off someone else's football?"),
    ("Rin Itoshi", "If you're not the main character of your own story, then what's the point?"),
    ("Meguru Bachira", "If you listen to your inner voice, the monster inside you will never die."),
    ("Meguru Bachira", "I just want to play with people who move the same way as my heartbeat."),
]


def get_result_loser_quote(match):
    if not match.get("winner"):
        return ""

    if not match.get("loser_quote"):
        speaker, quote = random.choice(LOSER_QUOTES)
        match["loser_quote"] = {"speaker": speaker, "quote": quote}

    loser = None
    winner_id = str(match.get("winner", {}).get("id", ""))

    for player_key in ("player_one", "player_two"):
        player = match.get(player_key)

        if player and str(player.get("id")) != winner_id:
            loser = player
            break

    if not loser:
        return ""

    quote_data = match["loser_quote"]
    return f"{player_result_name(loser)}, {quote_data['quote']}"


def make_match_result_embed(tournament, match, title="Match Result", note=None, card_filename=None):
    clean_embed = brand_embed(discord.Embed(
        description=f"**{tournament['name']}** | Round **{match.get('round')}**",
        color=random_embed_color(),
    ))

    if card_filename:
        clean_embed.set_image(url=f"attachment://{card_filename}")

    if match.get("dq"):
        clean_embed.add_field(name="Type", value="Disqualification", inline=True)

    loser_quote = get_result_loser_quote(match)

    if loser_quote:
        clean_embed.add_field(name="\u200b", value=loser_quote[:1024], inline=False)

    if note:
        clean_embed.add_field(name="Note", value=note[:1024], inline=False)

    return clean_embed

def apply_score_to_match(match, match_player_one_goals, match_player_two_goals):
    match["score"] = {
        "player_one": match_player_one_goals,
        "player_two": match_player_two_goals,
    }

    if match_player_one_goals == match_player_two_goals:
        match["winner"] = None
        match["state"] = "draw"
        return "draw"

    if match_player_one_goals > match_player_two_goals:
        match["winner"] = match.get("player_one")
    else:
        match["winner"] = match.get("player_two")

    match["state"] = "completed"
    return "completed"


async def post_match_result(guild, tournament, match, title="Match Result", note=None):
    channel = get_tournament_channel(guild, tournament, "results")
    card = await asyncio.to_thread(make_result_card_file, guild, tournament, match)
    card_file = card[0] if card else None
    card_filename = card[1] if card else None
    embed = make_match_result_embed(tournament, match, title=title, note=note, card_filename=card_filename)

    if channel:
        if card_file:
            await channel.send(embed=embed, file=card_file)
        else:
            await channel.send(embed=embed)
        return True

    return False


async def finalize_tournament_match(guild, tournament, match, result_message=None, title="Match Result"):
    match["state"] = "completed"
    match.pop("pending_score", None)

    if tournament.get("test_mode"):
        match.pop("profile_rewards", None)
    else:
        apply_match_profile_rewards(tournament, match)

    challonge_warning = None

    if tournament.get("challonge_url") and CHALLONGE_API_KEY:
        try:
            challonge_warning = await sync_challonge_v1_score(tournament, match)
        except RuntimeError as error:
            challonge_warning = str(error)

    note = None

    if challonge_warning:
        note = f"Local bracket updated, but Challonge was not updated: {challonge_warning}"
    elif tournament.get("challonge_url") and CHALLONGE_API_KEY:
        note = "Score synced to Challonge."

    if tournament.get("test_mode"):
        test_note = "Test mode is ON: profiles were not updated."
        note = f"{note}\n{test_note}" if note else test_note

    if result_message:
        try:
            card = await asyncio.to_thread(make_result_card_file, guild, tournament, match)
            card_file = card[0] if card else None
            card_filename = card[1] if card else None

            edit_kwargs = {
                "content": None,
                "embed": make_match_result_embed(tournament, match, title=title, note=note, card_filename=card_filename),
                "view": None,
                "allowed_mentions": discord.AllowedMentions.none(),
            }

            if card_file:
                edit_kwargs["attachments"] = [card_file]

            await result_message.edit(
                **edit_kwargs,
            )
        except discord.HTTPException:
            await post_match_result(guild, tournament, match, title=title, note=note)
    else:
        await post_match_result(guild, tournament, match, title=title, note=note)

    if not tournament.get("test_mode"):
        await post_updated_match_profiles(guild, tournament, match)

    await upsert_round_control_center(guild, tournament)
    return challonge_warning


def make_admin_panel_embed(guild, tournament):
    status = str(tournament.get("status", "setup")).title()
    players = tournament.get("players", [])
    current_round = tournament.get("current_round", 0)
    round_matches = get_current_round_matches(tournament) if tournament.get("rounds") else []
    completed_matches = sum(1 for match in round_matches if match.get("state") == "completed")
    total_matches = len(round_matches)
    inscriptions_channel = get_tournament_channel(guild, tournament, "inscriptions")
    results_channel = get_tournament_channel(guild, tournament, "results")
    challonge_status = tournament.get("challonge_url") or "Not linked"

    if tournament.get("status") == "setup":
        next_step = "`/register`, `/challonge_create`, then press Start Tournament when ready."
    elif tournament.get("status") == "running" and total_matches and completed_matches < total_matches:
        next_step = "`/score` or `/dq` for remaining matches."
    elif tournament.get("status") == "running":
        next_step = "`/next_round`"
    elif tournament.get("status") == "completed":
        next_step = "`/tournament_end` when you are done."
    else:
        next_step = "`/tournament_create`"

    embed = brand_embed(discord.Embed(
        title=f"\U0001F6E0\uFE0F Admin Panel - {tournament['name']}",
        description="Tournament control overview",
        color=random_embed_color(),
    ))
    embed.add_field(name="Status", value=f"**{status}**", inline=True)
    embed.add_field(name="Players", value=f"**{len(players)}**", inline=True)
    embed.add_field(name="Round", value=f"**{current_round or '-'}**", inline=True)
    embed.add_field(name="Start Time", value=tournament.get("start_time", "Not set"), inline=False)
    embed.add_field(
        name="Channels",
        value=(
            f"Inscriptions: {inscriptions_channel.mention if inscriptions_channel else 'Not set'}\n"
            f"Results: {results_channel.mention if results_channel else 'Not set'}\n"
            "Round control: registration hub after start"
        ),
        inline=False,
    )
    embed.add_field(name="Challonge", value=challonge_status, inline=False)

    if total_matches:
        embed.add_field(
            name="Round Progress",
            value=f"`{make_progress_bar(completed_matches, total_matches)}` {completed_matches}/{total_matches}",
            inline=False,
        )

    embed.add_field(name="Recommended Next Step", value=next_step, inline=False)
    return embed

def make_tournament_embed(tournament, guild=None):
    status = str(tournament.get("status", "setup")).title()
    players = tournament.get("players", [])
    embed = brand_embed(discord.Embed(
        title=f"\u2B50 {tournament['name']} \u2B50",
        description="Registration phase" if tournament.get("status") == "setup" else "Tournament control center",
        color=random_embed_color(),
    ))
    info_lines = [f"**Status:** {status}"]

    if tournament.get("test_mode"):
        info_lines.append("**Test Mode:** ON - profile rewards disabled")

    if tournament.get("start_time"):
        info_lines.append(f"**Start Time:** {tournament['start_time']}")

    if tournament.get("challonge_url"):
        info_lines.append(f"**Challonge:** [Open Bracket]({tournament['challonge_url']})")
    elif tournament.get("challonge_error"):
        info_lines.append(f"**Challonge:** Error - {tournament['challonge_error'][:160]}")
    elif not CHALLONGE_API_KEY:
        info_lines.append("**Challonge:** API key missing")
    elif len(players) < 2:
        info_lines.append("**Challonge:** Waiting for 2 registered players")
    else:
        info_lines.append("**Challonge:** Ready to create")

    embed.add_field(name="Tournament Info", value="\n".join(info_lines), inline=False)

    registration = tournament.get("registration", {})
    role_id = registration.get("role_id")
    role = None

    if guild and role_id and str(role_id).isdigit():
        role = guild.get_role(int(role_id))

    embed.add_field(
        name="Entry Role",
        value=role.mention if role else "Not set. Organisers can use `/set_tournament_role`.",
        inline=False,
    )

    channels = tournament.get("channels", {})
    channel_lines = []

    for label, key in (("Inscriptions", "inscriptions"), ("Results", "results"), ("Profiles", "profiles")):
        channel_id = channels.get(key)

        if channel_id:
            channel_lines.append(f"**{label}:** <#{channel_id}>")

    if channel_lines:
        embed.add_field(name="Channels", value="\n".join(channel_lines), inline=False)

    if tournament.get("status") == "setup":
        embed.add_field(
            name="Registration",
            value=(
                f"Participants: **{len(players)}**\n"
                "Press **Join Tournament** below to register.\n"
                "Use `/participants` to preview the registered player list."
            ),
            inline=False,
        )
        embed.set_footer(text="Use the Start Tournament button when registration is ready.")
        return embed

    for round_matches in tournament.get("rounds", [])[-2:]:
        if not round_matches:
            continue

        round_number = round_matches[0]["round"]
        lines = []

        for match in round_matches:
            player_one = tournament_player_label(match.get("player_one"), guild)
            player_two = tournament_player_label(match.get("player_two"), guild)
            winner = match.get("winner")
            status_icon = "\u2705 Done" if match.get("state") == "completed" else "\u2694\uFE0F Open"
            score = match.get("score")
            score_text = ""

            if isinstance(score, dict):
                score_text = f" | Score: **{score.get('player_one', 0)}-{score.get('player_two', 0)}**"

            if winner:
                lines.append(f"\u2B50 {player_one} vs {player_two}{score_text}\n**{status_icon} | Winner: {tournament_player_label(winner, guild)}**")
            elif match.get("state") == "draw":
                lines.append(f"\u2B50 {player_one} vs {player_two}{score_text}\n**\U0001F91D Draw - replay needed**")
            else:
                lines.append(f"\u2B50 {player_one} vs {player_two}\n**{status_icon}**")

        embed.add_field(
            name=f"\u2728 Round {round_number}",
            value="\n".join(lines)[:1024],
            inline=False,
        )

    if tournament.get("winner"):
        embed.add_field(
            name="\U0001F3C6 Champion",
            value=f"\u2B50 {tournament_player_label(tournament['winner'], guild)} \u2B50",
            inline=False,
        )
    else:
        embed.set_footer(text="Use /score or /dq to record matches, then /next_round to advance.")

    return embed


def make_tournament_embeds(tournament, guild=None):
    embeds = [make_tournament_embed(tournament, guild)]

    if tournament.get("status") != "setup":
        return embeds

    players = tournament.get("players", [])
    player_lines = [
        f"\u2B50 {index}. {tournament_player_label(player, guild, prefer_mention=True)}"
        for index, player in enumerate(players, start=1)
    ]
    add_chunked_fields_to_embeds(
        embeds,
        f"{tournament['name']} registrations",
        f"Registered Players ({len(players)})",
        player_lines,
        "No players registered yet.",
    )

    return embeds


def make_tournament_registration_embed(guild, tournament, role, message, include_invite_image=True):
    description = message.strip() or "A new tournament is open for registration."
    embed = brand_embed(discord.Embed(
        title=f"\u2B50 {tournament['name']} Registration \u2B50",
        description=(
            f"**You have been invited to compete in {guild.name}.**\n\n"
            f"{description}\n\n"
            "Press the registration button below to lock in your spot, or unregister if your plans change."
        ),
        color=random_embed_color(),
    ))

    if include_invite_image and TOURNAMENT_INVITE_ICON_PATH.exists():
        embed.set_image(url=f"attachment://{TOURNAMENT_INVITE_ICON_NAME}")

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(
        name="\U0001F3DF\uFE0F Tournament",
        value=(
            f"**Format:** Single Elimination\n"
            f"**Status:** Registration Open\n"
            f"**Starts:** {tournament.get('start_time', 'To be announced')}"
        ),
        inline=False,
    )
    embed.add_field(
        name="\U0001F396\uFE0F Entry Role",
        value=f"You will receive **{role.name}** after joining.",
        inline=False,
    )
    embed.add_field(
        name="\u26A1 What Happens Next",
        value=(
            "1. Click **Register for Tournament**.\n"
            "2. The bot gives you the tournament role.\n"
            "3. Your name is added to the bracket list.\n"
            "4. Use **Unregister** if you need to back out before it starts."
        ),
        inline=False,
    )
    embed.add_field(
        name="\U0001F4CC Server",
        value=guild.name,
        inline=True,
    )
    embed.add_field(
        name="\U0001F514 Reminder",
        value="Make sure your DMs stay open for tournament updates.",
        inline=True,
    )
    embed.set_footer(text="CFI Endgame Tournament System")
    return embed

def make_tournament_registration_file():
    if not TOURNAMENT_INVITE_ICON_PATH.exists():
        return None

    return discord.File(TOURNAMENT_INVITE_ICON_PATH, filename=TOURNAMENT_INVITE_ICON_NAME)


def member_label(guild, player_id):
    member = guild.get_member(int(player_id)) if guild and str(player_id).isdigit() else None
    return member.display_name if member else str(player_id)


def player_display_label(guild, player_id, player_names=None):
    if player_names and str(player_id) in player_names:
        return player_names[str(player_id)]

    return member_label(guild, player_id)


def make_endgame_probability_embed(guild, player_ids, votes_by_user, player_names=None):
    total_votes = len(votes_by_user)
    embed = discord.Embed(
        title="CFI Endgame Win Probability",
        description="Vote for the player you think will win Endgame.",
        color=EMBED_COLOR,
    )

    for index, player_id in enumerate(player_ids, start=1):
        vote_count = sum(1 for voted_id in votes_by_user.values() if voted_id == player_id)
        probability = vote_count / total_votes * 100 if total_votes else 0
        label = player_display_label(guild, player_id, player_names)
        embed.add_field(
            name=f"{index}. {label}",
            value=f"Votes: **{vote_count}** | Probability: **{probability:.1f}%**",
            inline=False,
        )

    embed.set_footer(text=f"Total votes: {total_votes}")
    return embed


class EndgameProbabilityView(discord.ui.View):
    def __init__(self, guild, player_ids, player_names=None):
        super().__init__(timeout=None)
        self.guild = guild
        self.player_ids = player_ids
        self.player_names = player_names or {}
        self.votes_by_user = {}
        self.message = None
        self.lock = asyncio.Lock()

        options = [
            discord.SelectOption(
                label=player_display_label(guild, player_id, self.player_names)[:100],
                value=player_id,
            )
            for player_id in player_ids
        ]
        select = discord.ui.Select(
            placeholder="Choose who you think will win Endgame",
            min_values=1,
            max_values=1,
            options=options,
        )
        select.callback = self.vote
        self.add_item(select)

    async def vote(self, interaction):
        selected_player_id = interaction.data["values"][0]
        await interaction.response.defer(ephemeral=True)

        async with self.lock:
            self.votes_by_user[interaction.user.id] = selected_player_id

            if self.message:
                await self.message.edit(
                    embed=make_endgame_probability_embed(
                        self.guild,
                        self.player_ids,
                        self.votes_by_user,
                        self.player_names,
                    ),
                    view=self,
                    allowed_mentions=discord.AllowedMentions.none(),
                )

        await interaction.followup.send("Your Endgame prediction has been counted.", ephemeral=True)


class TournamentRegistrationView(discord.ui.View):
    def __init__(self, guild_id, role_id, tournament_id):
        super().__init__(timeout=604800)
        self.guild_id = int(guild_id)
        self.role_id = int(role_id)
        self.tournament_id = str(tournament_id)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.label == "Register for Tournament":
                    item.custom_id = f"tournament_register:{self.guild_id}:{self.role_id}:{self.tournament_id}"
                elif item.label == "Unregister":
                    item.custom_id = f"tournament_unregister:{self.guild_id}:{self.role_id}:{self.tournament_id}"

    @discord.ui.button(label="Register for Tournament", style=discord.ButtonStyle.success, emoji="\u2705")
    async def join_tournament(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        guild = client.get_guild(self.guild_id)

        if not guild:
            await interaction.followup.send(
                "I cannot find the server for this tournament anymore.",
                ephemeral=True,
            )
            return

        role = guild.get_role(self.role_id)

        try:
            member = guild.get_member(interaction.user.id) or await guild.fetch_member(interaction.user.id)
        except discord.NotFound:
            await interaction.followup.send(
                "You are not in that server anymore, so I cannot register you.",
                ephemeral=True,
            )
            return

        role_note = ""

        if role:
            try:
                if role not in member.roles:
                    await member.add_roles(role, reason="Accepted tournament registration")
                role_note = f" You also received the **{role.name}** role."
            except (discord.Forbidden, discord.HTTPException):
                role_note = " I could not give the tournament role, but your registration was still saved."
        else:
            role_note = " The saved tournament role no longer exists, but your registration was still saved."

        async with TOURNAMENT_LOCK:
            tournaments = load_tournaments()
            tournament = tournaments.get("tournaments", {}).get(self.tournament_id)

            if not tournament:
                await interaction.followup.send(
                    "I could not find the tournament anymore.",
                    ephemeral=True,
                )
                return

            added, reason = add_member_to_tournament(tournament, member)

            if added:
                added_player = tournament["players"][-1]
                challonge_sync = None

                try:
                    if not tournament.get("challonge_url"):
                        challonge_sync = await ensure_setup_challonge_bracket(tournament)
                    else:
                        challonge_sync = await sync_new_player_to_challonge(tournament, added_player)
                except RuntimeError as error:
                    challonge_sync = f"failed: {error}"

                try:
                    await upsert_tournament_control_center(guild, tournament)
                except discord.HTTPException:
                    pass
                save_tournaments(tournaments)
                await interaction.followup.send(
                    f"You are registered for **{tournament['name']}**.{role_note}",
                    ephemeral=True,
                )
                return

            if reason == "exists":
                await interaction.followup.send(
                    f"You were already registered for **{tournament['name']}**.{role_note}",
                    ephemeral=True,
                )
                return

            await interaction.followup.send(
                f"Registration is closed for **{tournament['name']}**.",
                ephemeral=True,
            )

    @discord.ui.button(label="Unregister", style=discord.ButtonStyle.danger, emoji="\u274C")
    async def unregister_tournament(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        guild = client.get_guild(self.guild_id)

        if not guild:
            await interaction.followup.send(
                "I cannot find the server for this tournament anymore.",
                ephemeral=True,
            )
            return

        role = guild.get_role(self.role_id)

        try:
            member = guild.get_member(interaction.user.id) or await guild.fetch_member(interaction.user.id)
        except discord.NotFound:
            await interaction.followup.send(
                "You are not in that server anymore, so I cannot unregister you.",
                ephemeral=True,
            )
            return

        async with TOURNAMENT_LOCK:
            tournaments = load_tournaments()
            tournament = tournaments.get("tournaments", {}).get(self.tournament_id)

            if not tournament:
                await interaction.followup.send(
                    "I could not find the tournament anymore.",
                    ephemeral=True,
                )
                return

            if tournament.get("status") != "setup":
                await interaction.followup.send(
                    "The tournament has already started, so registration can no longer be changed.",
                    ephemeral=True,
                )
                return

            player_id = str(member.id)
            old_count = len(tournament.get("players", []))
            tournament["players"] = [
                player
                for player in tournament.get("players", [])
                if str(player.get("id")) != player_id
            ]
            removed_from_list = len(tournament["players"]) != old_count

            if role and role in member.roles:
                try:
                    await member.remove_roles(role, reason="Unregistered from tournament")
                except discord.Forbidden:
                    await interaction.followup.send(
                        "I removed you from the registration list, but I could not remove the role. Ask an admin to move my bot role above that role.",
                        ephemeral=True,
                    )
                    save_tournaments(tournaments)
                    return

            try:
                await upsert_tournament_control_center(guild, tournament)
            except discord.HTTPException:
                pass
            save_tournaments(tournaments)

        if removed_from_list:
            await interaction.followup.send(
                f"You are no longer registered for **{tournament['name']}**.",
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                f"You were not registered for **{tournament['name']}**.",
                ephemeral=True,
            )


async def send_registration_invites_background(guild_id, role_id, tournament_id, message, report_channel_id=None):
    guild = client.get_guild(int(guild_id))

    if not guild:
        return

    role = guild.get_role(int(role_id))

    if not role:
        return

    tournaments = load_tournaments()
    tournament = tournaments.get("tournaments", {}).get(str(tournament_id))

    if not tournament:
        return

    embed = make_tournament_registration_embed(guild, tournament, role, message)
    fallback_embed = make_tournament_registration_embed(guild, tournament, role, message, include_invite_image=False)
    sent_count = 0
    failed_count = 0
    skipped_count = 0
    failure_reasons = {}

    def count_failure(reason):
        failure_reasons[reason] = failure_reasons.get(reason, 0) + 1

    try:
        members = [member async for member in guild.fetch_members(limit=None)]
    except discord.HTTPException:
        members = list(guild.members)

    for member in members:
        if member.bot:
            skipped_count += 1
            continue

        view = TournamentRegistrationView(guild.id, role.id, tournament_id)

        try:
            invite_file = make_tournament_registration_file()

            if invite_file:
                await member.send(
                    content=f"{member.mention} \u26A1 your tournament invitation is here.",
                    embed=embed,
                    view=view,
                    file=invite_file,
                    allowed_mentions=discord.AllowedMentions(users=True),
                )
            else:
                await member.send(
                    content=f"{member.mention} \u26A1 your tournament invitation is here.",
                    embed=embed,
                    view=view,
                    allowed_mentions=discord.AllowedMentions(users=True),
                )

            sent_count += 1
        except discord.Forbidden as error:
            failed_count += 1
            count_failure(f"Forbidden {getattr(error, 'status', 403)}")
        except (discord.HTTPException, OSError) as error:
            try:
                await member.send(
                    content=f"{member.mention} \u26A1 your tournament invitation is here.",
                    embed=fallback_embed,
                    view=view,
                    allowed_mentions=discord.AllowedMentions(users=True),
                )
                sent_count += 1
            except discord.Forbidden as retry_error:
                failed_count += 1
                count_failure(f"Forbidden {getattr(retry_error, 'status', 403)}")
            except discord.HTTPException as retry_error:
                failed_count += 1
                status = getattr(retry_error, "status", "unknown")
                code = getattr(retry_error, "code", "unknown")
                count_failure(f"HTTP {status} code {code}")
            except OSError as retry_error:
                failed_count += 1
                count_failure(f"Network/File error {getattr(retry_error, 'errno', 'unknown')}")

        await asyncio.sleep(random.uniform(5, 15))

    report_channel = guild.get_channel(int(report_channel_id)) if report_channel_id else get_tournament_channel(guild, tournament, "inscriptions")

    if report_channel and is_tournament_post_channel(report_channel):
        try:
            reason_lines = [
                f"- {reason}: **{count}**"
                for reason, count in sorted(failure_reasons.items(), key=lambda item: item[1], reverse=True)[:5]
            ]
            advice = ""

            if sent_count == 0 and any(reason.startswith("Forbidden") for reason in failure_reasons):
                advice = (
                    "\n\nMost members blocked bot DMs or Discord blocked the mass DM attempt. "
                    "Use the public registration hub button as the main signup method for this server."
                )

            await report_channel.send(
                embed=make_embed(
                    "Registration DMs Finished",
                    (
                        f"Sent: **{sent_count}**\n"
                        f"Failed: **{failed_count}**\n"
                        f"Skipped bots: **{skipped_count}**"
                        + (f"\n\nFailure reasons:\n" + "\n".join(reason_lines) if reason_lines else "")
                        + advice
                    ),
                    SUCCESS_COLOR,
                ),
                allowed_mentions=discord.AllowedMentions.none(),
            )
        except discord.HTTPException:
            pass


class ScoreApprovalView(discord.ui.View):
    def __init__(self, tournament_id, match_id, opponent_id):
        super().__init__(timeout=86400)
        self.tournament_id = str(tournament_id)
        self.match_id = str(match_id)
        self.opponent_id = str(opponent_id)

    async def _load_pending_match(self, interaction):
        tournaments = load_tournaments()
        tournament = tournaments.get("tournaments", {}).get(self.tournament_id)

        if not tournament:
            await interaction.followup.send("I could not find this tournament anymore.", ephemeral=True)
            return None, None, None

        match = find_tournament_match(tournament, self.match_id)

        if not match or match.get("state") not in ("open", "draw"):
            await interaction.followup.send("This match is no longer open.", ephemeral=True)
            return tournaments, tournament, None

        if not match.get("pending_score"):
            await interaction.followup.send("There is no pending score to review anymore.", ephemeral=True)
            return tournaments, tournament, None

        if str(interaction.user.id) != self.opponent_id and not has_command_role_access(interaction):
            await interaction.followup.send("Only the opponent or a tournament organiser can accept or reject this score.", ephemeral=True)
            return tournaments, tournament, None

        return tournaments, tournament, match

    @discord.ui.button(label="Accept Score", style=discord.ButtonStyle.success, emoji="\u2705")
    async def accept_score(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        async with TOURNAMENT_LOCK:
            tournaments, tournament, match = await self._load_pending_match(interaction)

            if not match:
                return

            pending_score = match["pending_score"]
            record_undo("accept tournament score", profiles=load_profiles(), tournaments=tournaments)
            result_state = apply_score_to_match(
                match,
                int(pending_score["player_one"]),
                int(pending_score["player_two"]),
            )

            if result_state == "draw":
                match.pop("pending_score", None)
                try:
                    card = await asyncio.to_thread(make_result_card_file, interaction.guild, tournament, match)
                    card_file = card[0] if card else None
                    card_filename = card[1] if card else None
                    edit_kwargs = {
                        "content": None,
                        "embed": make_match_result_embed(
                            tournament,
                            match,
                            title="Draw Accepted",
                            note="Replay needed before this match can advance.",
                            card_filename=card_filename,
                        ),
                        "view": None,
                        "allowed_mentions": discord.AllowedMentions.none(),
                    }

                    if card_file:
                        edit_kwargs["attachments"] = [card_file]

                    await interaction.message.edit(
                        **edit_kwargs,
                    )
                except discord.HTTPException:
                    await post_match_result(
                        interaction.guild,
                        tournament,
                        match,
                        title="Draw Accepted",
                        note="Replay needed before this match can advance.",
                    )
                await upsert_round_control_center(interaction.guild, tournament)
            else:
                await finalize_tournament_match(
                    interaction.guild,
                    tournament,
                    match,
                    result_message=interaction.message,
                )

            save_tournaments(tournaments)

        await interaction.followup.send("Score accepted and recorded.", ephemeral=True)

    @discord.ui.button(label="Reject Score", style=discord.ButtonStyle.danger, emoji="\u274C")
    async def reject_score(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        async with TOURNAMENT_LOCK:
            tournaments, tournament, match = await self._load_pending_match(interaction)

            if not match:
                return

            record_undo("reject tournament score", tournaments=tournaments)
            match.pop("pending_score", None)
            save_tournaments(tournaments)
            await upsert_round_control_center(interaction.guild, tournament)

        try:
            await interaction.message.edit(
                content=None,
                embed=make_embed("Score Rejected", "The reported score was rejected. The match is still open.", ERROR_COLOR),
                view=None,
                allowed_mentions=discord.AllowedMentions.none(),
            )
        except discord.HTTPException:
            pass

        await interaction.followup.send("Score rejected. The match is still open.", ephemeral=True)


async def start_tournament_from_hub(interaction, tournament_id, hub_channel_id, hub_message_id):
    async with TOURNAMENT_LOCK:
        tournaments = load_tournaments()
        tournament = tournaments.get("tournaments", {}).get(str(tournament_id))

        if not tournament:
            await interaction.followup.send("I could not find this tournament anymore.", ephemeral=True)
            return

        if not has_command_role_access(interaction):
            await interaction.followup.send("Only tournament organisers can use this control.", ephemeral=True)
            return

        if tournament.get("status") != "setup":
            await interaction.followup.send("This tournament has already started.", ephemeral=True)
            return

        if len(tournament.get("players", [])) < 2:
            await interaction.followup.send("Add at least 2 players before starting.", ephemeral=True)
            return

        record_undo("start tournament from hub", tournaments=tournaments)
        start_tournament_bracket(tournament, shuffle_players=False)
        challonge_note = None
        tournament_identifier = get_challonge_identifier_from_tournament(tournament)

        if tournament_identifier and CHALLONGE_API_KEY and not tournament.get("challonge", {}).get("started"):
            try:
                await start_challonge_v1_tournament(tournament_identifier)
                tournament.setdefault("challonge", {})["started"] = True
                challonge_note = "Challonge bracket started."
            except RuntimeError as error:
                challonge_note = f"Local bracket started, but Challonge did not start: {error}"

        messages = tournament.setdefault("messages", {})
        messages["control_center"] = str(hub_message_id)

        round_control_channel = get_tournament_channel(interaction.guild, tournament, "round_control")

        if round_control_channel and round_control_channel.id == int(hub_channel_id):
            messages["round_control"] = str(hub_message_id)
        elif round_control_channel:
            await upsert_round_control_center(interaction.guild, tournament)

        save_tournaments(tournaments)

    embeds = make_round_control_embeds(tournament, interaction.guild)
    embed = embeds[0]

    if challonge_note:
        embed.add_field(name="Challonge", value=challonge_note[:1024], inline=False)

    try:
        channel = interaction.guild.get_channel(int(hub_channel_id)) if interaction.guild else None
        if channel is None and interaction.guild:
            channel = await interaction.guild.fetch_channel(int(hub_channel_id))
        if channel:
            message = await channel.fetch_message(int(hub_message_id))
            await message.edit(embed=embed, view=None)
            messages = tournament.setdefault("messages", {})
            messages["round_control"] = str(message.id)
            await sync_round_control_extra_embeds(channel, messages, embeds[1:])
            save_tournaments(tournaments)
    except (discord.HTTPException, ValueError, TypeError):
        pass

    await interaction.followup.send("Tournament started. The registration hub is now round control.", ephemeral=True)


class StartTournamentConfirmView(discord.ui.View):
    def __init__(self, tournament_id, requester_id, hub_channel_id, hub_message_id):
        super().__init__(timeout=60)
        self.tournament_id = str(tournament_id)
        self.requester_id = int(requester_id)
        self.hub_channel_id = int(hub_channel_id)
        self.hub_message_id = int(hub_message_id)

    async def interaction_check(self, interaction):
        if interaction.user.id != self.requester_id:
            await interaction.response.send_message(
                "Only the organiser who opened this confirmation can use it.",
                ephemeral=True,
            )
            return False
        return True

    @discord.ui.button(label="Yes, Start Tournament", style=discord.ButtonStyle.danger, emoji="\u2694\uFE0F")
    async def confirm_start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        for item in self.children:
            item.disabled = True

        try:
            await interaction.message.edit(view=self)
        except discord.HTTPException:
            pass

        await start_tournament_from_hub(
            interaction,
            self.tournament_id,
            self.hub_channel_id,
            self.hub_message_id,
        )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary, emoji="\u274C")
    async def cancel_start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        for item in self.children:
            item.disabled = True

        try:
            await interaction.message.edit(content="Tournament start cancelled.", embed=None, view=self)
        except discord.HTTPException:
            pass

        await interaction.followup.send("Cancelled. Registration stays open.", ephemeral=True)


class TournamentHubView(discord.ui.View):
    def __init__(self, tournament_id):
        super().__init__(timeout=None)
        self.tournament_id = str(tournament_id)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.label == "Join Tournament":
                    item.custom_id = f"tournament_hub_join:{self.tournament_id}"
                elif item.label == "Start Tournament":
                    item.custom_id = f"tournament_hub_start:{self.tournament_id}"
                elif item.label == "Refresh":
                    item.custom_id = f"tournament_hub_refresh:{self.tournament_id}"

    async def _load_setup_tournament(self, interaction):
        tournaments = load_tournaments()
        tournament = tournaments.get("tournaments", {}).get(self.tournament_id)

        if not tournament:
            await interaction.followup.send("I could not find this tournament anymore.", ephemeral=True)
            return None, None

        if not has_command_role_access(interaction):
            await interaction.followup.send("Only tournament organisers can use this control.", ephemeral=True)
            return tournaments, None

        if tournament.get("status") != "setup":
            await interaction.followup.send("This tournament has already started.", ephemeral=True)
            return tournaments, None

        return tournaments, tournament

    @discord.ui.button(label="Join Tournament", style=discord.ButtonStyle.primary, emoji="\u2B50")
    async def join_tournament_from_hub(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        if not interaction.guild:
            await interaction.followup.send("This button can only be used inside a server.", ephemeral=True)
            return

        async with TOURNAMENT_LOCK:
            tournaments = load_tournaments()
            tournament = tournaments.get("tournaments", {}).get(self.tournament_id)

            if not tournament:
                await interaction.followup.send("I could not find this tournament anymore.", ephemeral=True)
                return

            if tournament.get("status") != "setup":
                await interaction.followup.send("This tournament has already started.", ephemeral=True)
                return

            registration = tournament.get("registration", {})
            role_id = registration.get("role_id")
            role = interaction.guild.get_role(int(role_id)) if role_id and str(role_id).isdigit() else None

            try:
                member = interaction.guild.get_member(interaction.user.id) or await interaction.guild.fetch_member(interaction.user.id)
            except discord.NotFound:
                await interaction.followup.send("I could not find you in this server anymore.", ephemeral=True)
                return

            role_note = ""

            if role:
                try:
                    if role not in member.roles:
                        await member.add_roles(role, reason="Joined tournament from registration hub")
                    role_note = f" You also received the **{role.name}** role."
                except (discord.Forbidden, discord.HTTPException):
                    role_note = " I could not give the tournament role, but your registration was still saved."
            else:
                role_note = " No tournament role is saved anymore, but your registration was still saved."

            added, reason = add_member_to_tournament(tournament, member)

            if added:
                added_player = tournament["players"][-1]

                try:
                    if not tournament.get("challonge_url"):
                        await ensure_setup_challonge_bracket(tournament)
                    else:
                        await sync_new_player_to_challonge(tournament, added_player)
                except RuntimeError as error:
                    try:
                        await upsert_tournament_control_center(interaction.guild, tournament)
                    except discord.HTTPException:
                        pass
                    save_tournaments(tournaments)
                    await interaction.followup.send(
                        f"You joined **{tournament['name']}**.{role_note} Challonge sync warned: {error}",
                        ephemeral=True,
                    )
                    return

                try:
                    await upsert_tournament_control_center(interaction.guild, tournament)
                except discord.HTTPException:
                    pass
                save_tournaments(tournaments)
                await interaction.followup.send(
                    f"You joined **{tournament['name']}**.{role_note}",
                    ephemeral=True,
                )
                return

            if reason == "exists":
                try:
                    await upsert_tournament_control_center(interaction.guild, tournament)
                except discord.HTTPException:
                    pass
                save_tournaments(tournaments)
                await interaction.followup.send(
                    f"You are already registered for **{tournament['name']}**.{role_note}",
                    ephemeral=True,
                )
                return

            await interaction.followup.send(
                "Registration is closed.",
                ephemeral=True,
            )

    @discord.ui.button(label="Start Tournament", style=discord.ButtonStyle.danger, emoji="\u2694\uFE0F")
    async def start_tournament(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        tournaments, tournament = await self._load_setup_tournament(interaction)

        if not tournament:
            return

        player_count = len(tournament.get("players", []))

        if player_count < 2:
            await interaction.followup.send("Add at least 2 players before starting.", ephemeral=True)
            return

        confirm_embed = make_embed(
            "Start Tournament?",
            (
                f"Are you sure you want to start **{tournament['name']}** with **{player_count}** players?\n\n"
                "This closes registration and turns the hub into round control."
            ),
            ERROR_COLOR,
        )
        confirm_view = StartTournamentConfirmView(
            self.tournament_id,
            interaction.user.id,
            interaction.channel_id,
            interaction.message.id,
        )
        await interaction.followup.send(embed=confirm_embed, view=confirm_view, ephemeral=True)

    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.secondary, emoji="\U0001F504")
    async def refresh_tournament(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        tournaments = load_tournaments()
        tournament = tournaments.get("tournaments", {}).get(self.tournament_id)

        if not tournament:
            await interaction.followup.send("I could not find this tournament anymore.", ephemeral=True)
            return

        embeds = make_tournament_embeds(tournament, interaction.guild) if tournament.get("status") == "setup" else make_round_control_embeds(tournament, interaction.guild)
        embed = embeds[0]
        view = self if tournament.get("status") == "setup" else None

        try:
            await interaction.message.edit(embed=embed, view=view)
            messages = tournament.setdefault("messages", {})
            if tournament.get("status") == "setup":
                await sync_control_center_extra_embeds(interaction.channel, messages, embeds[1:])
                await sync_round_control_extra_embeds(interaction.channel, messages, [])
                save_tournaments(tournaments)
            else:
                messages["round_control"] = str(interaction.message.id)
                await sync_control_center_extra_embeds(interaction.channel, messages, [])
                await sync_round_control_extra_embeds(interaction.channel, messages, embeds[1:])
                save_tournaments(tournaments)
        except discord.HTTPException:
            await interaction.followup.send("I could not refresh this message.", ephemeral=True)
            return

        await interaction.followup.send("Refreshed.", ephemeral=True)


class MatchVoteView(discord.ui.View):
    def __init__(self, match_id, player_one, player_two):
        super().__init__(timeout=None)
        self.match_id = match_id
        self.player_one = player_one
        self.player_two = player_two
        self.votes_by_user = {}
        self.message = None
        self.closed = False
        self.confirmed = False
        self.lock = asyncio.Lock()

        player_one_button = discord.ui.Button(
            label=player_one.display_name[:80],
            style=discord.ButtonStyle.primary,
        )
        player_two_button = discord.ui.Button(
            label=player_two.display_name[:80],
            style=discord.ButtonStyle.primary,
        )
        player_one_button.callback = self.vote_for_player_one
        player_two_button.callback = self.vote_for_player_two
        self.add_item(player_one_button)
        self.add_item(player_two_button)

    async def vote_for_player_one(self, interaction):
        await self.record_vote(interaction, self.player_one.id)

    async def vote_for_player_two(self, interaction):
        await self.record_vote(interaction, self.player_two.id)

    async def record_vote(self, interaction, player_id):
        if self.closed:
            await interaction.response.send_message(
                "This vote is already closed.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        async with self.lock:
            voter_id = interaction.user.id
            self.votes_by_user[voter_id] = player_id

            player_one_votes = sum(
                1 for voted_player_id in self.votes_by_user.values()
                if voted_player_id == self.player_one.id
            )
            player_two_votes = sum(
                1 for voted_player_id in self.votes_by_user.values()
                if voted_player_id == self.player_two.id
            )

            print(
                f"Vote from {interaction.user} for {player_id}. "
                f"{self.player_one.display_name}: {player_one_votes}, "
                f"{self.player_two.display_name}: {player_two_votes}, "
                f"total unique voters: {len(self.votes_by_user)}"
            )

            if self.message:
                await self.message.edit(
                    embed=make_vote_embed(
                        self.player_one,
                        self.player_two,
                        self.votes_by_user,
                        match_id=self.match_id,
                    ),
                    view=self,
                    allowed_mentions=discord.AllowedMentions.none(),
                )

        await interaction.followup.send(
            "Your vote has been counted.",
            ephemeral=True,
        )

    async def close_vote(self):
        if self.closed:
            return

        self.closed = True

        for item in self.children:
            item.disabled = True

        if self.message:
            await self.message.edit(
                content="Match vote closed.",
                embed=make_vote_embed(
                    self.player_one,
                    self.player_two,
                    self.votes_by_user,
                    closed=True,
                    match_id=self.match_id,
                    confirmed=self.confirmed,
                ),
                view=self,
                allowed_mentions=discord.AllowedMentions.none(),
            )

        self.stop()

    async def close_after_delay(self, seconds):
        await asyncio.sleep(seconds)
        await self.close_vote()


async def clan_autocomplete(interaction, current):
    search = current.lower()
    matches = [clan for clan in CLANS if search in clan.lower()]
    return [
        discord.app_commands.Choice(name=clan[:100], value=clan)
        for clan in matches[:25]
    ]


async def country_autocomplete(interaction, current):
    search = current.lower().strip()
    options = []

    for country_name, country_code in COUNTRIES.items():
        label = f"{country_flag(country_code)} {country_name}"

        if not search or search in country_name.lower() or search == country_code.lower():
            options.append(discord.app_commands.Choice(name=label[:100], value=country_name))

    if not search or "none".startswith(search):
        options.insert(0, discord.app_commands.Choice(name="None", value="None"))

    return options[:25]


@client.event
async def on_ready():
    tournaments = load_tournaments()
    restored_hubs = 0

    for tournament_id, tournament in tournaments.get("tournaments", {}).items():
        if tournament.get("status") != "setup":
            continue

        message_id = tournament.get("messages", {}).get("control_center")

        if not message_id or not str(message_id).isdigit():
            continue

        try:
            client.add_view(TournamentHubView(tournament_id), message_id=int(message_id))
            restored_hubs += 1
        except ValueError:
            pass

    synced_commands = await tree.sync()
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("Synced commands: " + ", ".join(f"/{command.name}" for command in synced_commands))
    print(f"Restored tournament registration hubs: {restored_hubs}")
    print("Bot is ready. Try typing /show_leaderboard in your Discord server.")


@tree.command(name="ping", description="Check whether the bot is online.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


@tree.command(name="help", description="Show the tournament bot flow and key commands.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="CFI Endgame Help",
        description="Clean tournament flow and command guide.",
        color=random_embed_color(),
    )
    embed.add_field(
        name="1. Setup",
        value=(
            "`/set_tournament_organizer_role` - choose organiser role\n"
            "`/tournament_create` - choose inscriptions, results, and profiles channels\n"
            "`/test_mode` - optional testing without profile rewards"
        ),
        inline=False,
    )
    embed.add_field(
        name="2. Registration",
        value=(
            "`/register` - send tournament invites with Register/Unregister buttons\n"
            "`/registration_hub` - post a clean public register button without the full player list\n"
            "`/tournament_add` / `/drop` - organiser manual edits\n"
            "`/participants` / `/participants_export` - check registration\n"
            "The main control hub updates live with joined players."
        ),
        inline=False,
    )
    embed.add_field(
        name="3. Tournament",
        value=(
            "Press **Start Tournament** on the hub.\n"
            "`/score` - players submit score; opponent accepts/rejects\n"
            "`/dq` - organiser disqualifies a missing player\n"
            "`/next_round` - advance and DM next opponents"
        ),
        inline=False,
    )
    embed.add_field(
        name="4. Profiles",
        value=(
            "`/show_profile` - view a profile\n"
            "`/edit_profile` - choose clan and profile image/GIF\n"
            "`/admin_edit_profile` - organiser profile corrections\n"
            "`/mygrade` - view a player's Player Grade\n"
            "`/player_grades` - view the Player Grade ladder\n"
            "`/set_player_grade_gif` - organiser Player Grade GIFs\n"
            "`/set_player_grade_seed` - organiser starting GD reputation\n"
            "Profiles update automatically after real match results."
        ),
        inline=False,
    )
    embed.add_field(
        name="Reset / Safety",
        value=(
            "`/undo_last` - undo the last important action\n"
            "`/tournament_end` - end active tournament\n"
            "`/tournament_hub_repost` - repost the hub cleanly\n"
            "`/tournament_channels` - change inscriptions/results/profiles channels"
        ),
        inline=False,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="test_mode", description="Turn test mode on/off for the active tournament.")
async def test_mode(interaction: discord.Interaction, enabled: bool):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "Create a tournament first with `/tournament_create`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("toggle test mode", tournaments=tournaments)
    tournament["test_mode"] = bool(enabled)
    await upsert_tournament_control_center(interaction.guild, tournament)

    if tournament.get("status") != "setup":
        await upsert_round_control_center(interaction.guild, tournament)

    save_tournaments(tournaments)

    status = "ON" if enabled else "OFF"
    detail = (
        "Profile rewards, records, finishes, and profile auto-posts are disabled."
        if enabled
        else "Future completed matches will update profiles normally again."
    )
    await interaction.followup.send(
        embed=make_embed(f"Test Mode {status}", detail, SUCCESS_COLOR),
        ephemeral=True,
    )


@tree.command(name="set_command_role", description="Set the role allowed to use admin/data-changing bot commands.")
async def set_command_role(interaction: discord.Interaction, role: discord.Role):
    can_reply = True

    try:
        await interaction.response.defer(ephemeral=True)
    except discord.NotFound:
        can_reply = False
        print("set_command_role interaction expired before it could be acknowledged; saving setting anyway.")

    async def reply_private(embed):
        if not can_reply:
            return

        try:
            await interaction.followup.send(embed=embed, ephemeral=True)
        except discord.NotFound:
            print("set_command_role could not send private confirmation because the interaction expired.")

    if not isinstance(interaction.user, discord.Member) or not interaction.user.guild_permissions.manage_guild:
        await reply_private(
            make_embed(
                "Missing Permission",
                "You need Manage Server to set the command role.",
                ERROR_COLOR,
            )
        )
        return

    settings = load_settings()
    settings["command_role_id"] = role.id
    save_settings(settings)

    await reply_private(
        make_embed(
            "Command Role Set",
            f"Admin/data-changing commands now require {role.mention}.",
            SUCCESS_COLOR,
        )
    )


@tree.command(name="set_tournament_organizer_role", description="Set the role allowed to manage tournament data.")
async def set_tournament_organizer_role(interaction: discord.Interaction, role: discord.Role):
    if not await safe_defer(interaction):
        return

    if not isinstance(interaction.user, discord.Member) or not interaction.user.guild_permissions.manage_guild:
        await interaction.followup.send(
            embed=make_embed(
                "Missing Permission",
                "You need Manage Server to set the tournament organiser role.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    settings = load_settings()
    settings["tournament_organizer_role_id"] = role.id
    settings["command_role_id"] = role.id
    save_settings(settings)

    await interaction.followup.send(
        embed=make_embed(
            "Tournament Organiser Role Set",
            f"Data-changing tournament commands now require {role.mention}.",
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="set_result_gif", description="Set the GIF/image used under match result embeds.")
async def set_result_gif(interaction: discord.Interaction, url: str):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    clean_url = url.strip()
    settings = load_settings()

    if clean_url.lower() in {"none", "clear", "remove", "off"}:
        settings.pop("result_media_url", None)
        save_settings(settings)
        await interaction.followup.send(
            embed=make_embed(
                "Result GIF Cleared",
                "Match results will now use the normal clean embed without a custom GIF.",
                SUCCESS_COLOR,
            ),
            ephemeral=True,
        )
        return

    if len(clean_url) > 1000:
        await interaction.followup.send(
            embed=make_embed("URL Too Long", "Keep the result GIF URL under 1000 characters.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if not is_valid_profile_url(clean_url):
        await interaction.followup.send(
            embed=make_embed("Invalid URL", "Use a full link starting with `https://` or `http://`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    clean_url = await asyncio.to_thread(resolve_profile_media_url, clean_url)

    if not is_direct_media_url(clean_url):
        await interaction.followup.send(
            embed=make_embed(
                "Direct Media Needed",
                "Use a Discord GIF/image link, Tenor GIF, Giphy link, or direct `.png`, `.jpg`, `.gif`, or `.webp` URL.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    settings["result_media_url"] = clean_url
    save_settings(settings)

    preview = make_embed(
        "Result GIF Set",
        "This media will now show under match result embeds.",
        SUCCESS_COLOR,
    )
    preview.set_image(url=clean_url)

    await interaction.followup.send(embed=preview, ephemeral=True)


@tree.command(name="set_player_grade_gif", description="Set the GIF/image used for a player grade.")
@discord.app_commands.choices(grade=[
    discord.app_commands.Choice(name="Trash", value="trash"),
    discord.app_commands.Choice(name="World Class", value="world_class"),
    discord.app_commands.Choice(name="Generational", value="generational"),
    discord.app_commands.Choice(name="Legendary", value="legendary"),
])
async def set_player_grade_gif(interaction: discord.Interaction, grade: discord.app_commands.Choice[str], url: str):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    clean_url = url.strip()
    settings = load_settings()
    grade_gifs = settings.setdefault("player_grade_gifs", {})

    if clean_url.lower() in {"none", "clear", "remove", "off"}:
        grade_gifs.pop(grade.value, None)
        save_settings(settings)
        await interaction.followup.send(
            embed=make_embed(
                "Player Grade GIF Cleared",
                f"Removed the custom GIF for **{grade.name}**.",
                SUCCESS_COLOR,
            ),
            ephemeral=True,
        )
        return

    if len(clean_url) > 1000:
        await interaction.followup.send(
            embed=make_embed("URL Too Long", "Keep the Player Grade GIF URL under 1000 characters.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if not is_valid_profile_url(clean_url):
        await interaction.followup.send(
            embed=make_embed("Invalid URL", "Use a full link starting with `https://` or `http://`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    clean_url = await asyncio.to_thread(resolve_profile_media_url, clean_url)

    if not is_direct_media_url(clean_url):
        await interaction.followup.send(
            embed=make_embed(
                "Direct Media Needed",
                "Use a Discord GIF/image link, Tenor GIF, Giphy link, or direct `.png`, `.jpg`, `.gif`, or `.webp` URL.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    grade_gifs[grade.value] = clean_url
    save_settings(settings)

    preview = make_embed(
        "Player Grade GIF Set",
        f"This media will now be shown for **{grade.name}**.",
        SUCCESS_COLOR,
    )
    preview.set_image(url=clean_url)
    await interaction.followup.send(embed=preview, ephemeral=True)


@tree.command(name="mygrade", description="Show your current Player Grade.")
async def mygrade(interaction: discord.Interaction, player: Optional[discord.Member] = None):
    target = player or interaction.user
    profiles = load_profiles()
    profile = get_profile(profiles, target.id)
    grade_key, grade_label, _average_gd = get_profile_player_grade(profile)
    settings = load_settings()
    grade_gif = settings.get("player_grade_gifs", {}).get(grade_key, "")
    wins = int(profile.get("wins", 0) or 0)
    losses = int(profile.get("losses", 0) or 0)

    embed = make_embed(
        f"\u26A1 {target.display_name}'s Player Grade \u26A1",
        "This grade is earned through tournament performance.",
        SUCCESS_COLOR,
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="Player Grade", value=grade_label, inline=True)
    embed.add_field(name="Win-Loss Record", value=f"{wins}-{losses}", inline=True)

    if grade_gif:
        embed.set_image(url=grade_gif)
    else:
        embed.add_field(name="Grade GIF", value="No GIF has been set for this grade yet.", inline=False)

    await interaction.response.send_message(embed=embed)


@tree.command(name="player_grades", description="Show the Player Grade ladder and configured GIFs.")
async def player_grades(interaction: discord.Interaction):
    settings = load_settings()
    grade_gifs = settings.get("player_grade_gifs", {})
    grade_descriptions = {
        "legendary": "You are as close to unbeatable as it gets.",
        "generational": "You are beyond the standard that everyone else is chasing.",
        "world_class": "You are a proven force in any bracket.",
        "trash": "For players who still have to prove themselves on the pitch.",
    }
    lines = []

    for key, name, _minimum_gd, emoji in PLAYER_GRADE_TIERS:
        gif_status = "GIF set" if grade_gifs.get(key) else "no GIF yet"
        lines.append(f"{emoji} **{name}** - {grade_descriptions[key]} ({gif_status})")

    embed = make_embed(
        "Player Grades",
        "\n".join(lines),
        SUCCESS_COLOR,
    )
    embed.set_footer(text="Use /mygrade to view a player's current grade.")
    await interaction.response.send_message(embed=embed)


@tree.command(name="set_player_grade_seed", description="Give a player a starting GD reputation for Player Grade.")
async def set_player_grade_seed(
    interaction: discord.Interaction,
    player: discord.Member,
    average_gd: float,
    virtual_matches: int = 10,
):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    if virtual_matches < 0 or virtual_matches > 200:
        await interaction.followup.send(
            embed=make_embed("Invalid Match Weight", "Use a virtual match weight from 0 to 200.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if average_gd < -10 or average_gd > 10:
        await interaction.followup.send(
            embed=make_embed("Invalid GD", "Use an average GD between -10 and 10.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    profiles = load_profiles()
    profile = get_profile(profiles, player.id)
    profile["player_grade_seed_gd"] = round(float(average_gd), 3)
    profile["player_grade_seed_matches"] = int(virtual_matches)
    save_profiles(profiles)

    grade_key, grade_label, new_average_gd = get_profile_player_grade(profile)
    await interaction.followup.send(
        embed=make_embed(
            "Player Grade Seed Set",
            (
                f"{player.mention} now starts with **{average_gd:.2f} GD** over "
                f"**{virtual_matches} virtual matches**.\n"
                f"Current Player Grade: **{grade_label}** ({new_average_gd:.2f} average GD)."
            ),
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="anon_send", description="Send an anonymous bot message to a chosen channel.")
async def anon_send(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    message: str,
):
    can_reply = True

    try:
        await interaction.response.defer(ephemeral=True)
    except discord.NotFound:
        can_reply = False
        print("anon_send interaction expired before it could be acknowledged; sending message anyway.")

    async def reply_private(embed):
        if not can_reply:
            return

        try:
            await interaction.followup.send(embed=embed, ephemeral=True)
        except discord.NotFound:
            print("anon_send could not send private confirmation because the interaction expired.")

    if not await require_command_role(interaction):
        return

    clean_message = message.strip()

    if not clean_message:
        await reply_private(make_embed("Empty Message", "Message cannot be empty.", ERROR_COLOR))
        return

    if len(clean_message) > 2000:
        await reply_private(
            make_embed(
                "Message Too Long",
                "Discord messages cannot be longer than 2000 characters.",
                ERROR_COLOR,
            )
        )
        return

    try:
        await channel.send(
            clean_message,
            allowed_mentions=discord.AllowedMentions(
                everyone=False,
                users=False,
                roles=True,
            ),
        )
        print(f"Anonymous message sent by {interaction.user} to #{channel.name}")
    except discord.Forbidden:
        await reply_private(
            make_embed(
                "Missing Bot Permission",
                f"I cannot send messages or mention roles in {channel.mention}.",
                ERROR_COLOR,
            )
        )
        return
    except discord.HTTPException as error:
        print(f"anon_send failed: {error}")
        await reply_private(
            make_embed(
                "Message Failed",
                f"Discord rejected the message.\nError: `{error}`",
                ERROR_COLOR,
            )
        )
        return

    await reply_private(
        make_embed(
            "Message Sent",
            f"Sent anonymous message to {channel.mention}.",
            SUCCESS_COLOR,
        )
    )


@tree.command(name="score_add", description="Add score from a match percentage. 1 percent = 1000 score.")
async def score_add(interaction: discord.Interaction, player: discord.Member, percent: float):
    if not await require_command_role(interaction):
        return

    if percent < 0:
        await interaction.response.send_message(
            embed=make_embed("Invalid Percent", "Percent cannot be negative.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    added_score = round(percent * SCORE_PER_PERCENT)
    scores, old_score, new_score = add_prestige_to_member(player, added_score)

    summary = (
        f"Added **{percent:g}%** for {player.mention}.\n"
        f"Converted score: **{added_score}**\n"
        f"Previous total: **{old_score}**\n"
        f"New total: **{new_score}**"
    )

    await interaction.response.send_message(embed=make_leaderboard_embed(scores, summary))


@tree.command(name="start_vote", description="Start a 6-minute match vote between two players.")
async def start_vote(
    interaction: discord.Interaction,
    player_one: discord.Member,
    player_two: discord.Member,
):
    global NEXT_MATCH_ID

    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    if player_one.id == player_two.id:
        await interaction.followup.send(
            embed=make_embed(
                "Invalid Match",
                "Choose two different players.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    match_id = NEXT_MATCH_ID
    NEXT_MATCH_ID += 1

    view = MatchVoteView(match_id, player_one, player_two)
    MATCH_VOTES[match_id] = view

    try:
        view.message = await interaction.channel.send(
            content="@everyone Match vote started!",
            embed=make_vote_embed(player_one, player_two, view.votes_by_user, match_id=match_id),
            view=view,
            allowed_mentions=discord.AllowedMentions(everyone=True),
        )
    except discord.Forbidden:
        await interaction.followup.send(
            embed=make_embed(
                "Missing Permission",
                "I cannot send messages in this channel. Give me Send Messages and Embed Links.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    asyncio.create_task(view.close_after_delay(360))
    await interaction.followup.send(f"Vote started. Match ID: `{match_id}`.", ephemeral=True)


@tree.command(name="confirm_winner", description="Confirm the winner of a closed vote and add Prestige.")
async def confirm_winner(
    interaction: discord.Interaction,
    match_id: int,
    winner: discord.Member,
):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    vote = MATCH_VOTES.get(match_id)

    if not vote:
        await interaction.followup.send(
            embed=make_embed(
                "Match Not Found",
                f"I could not find match ID `{match_id}`. Votes only stay available while the bot is running.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if not vote.closed:
        await interaction.followup.send(
            embed=make_embed(
                "Vote Still Open",
                "Wait until the vote closes before confirming the winner.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if vote.confirmed:
        await interaction.followup.send(
            embed=make_embed(
                "Winner Already Confirmed",
                f"Match ID `{match_id}` has already been registered.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if winner.id not in (vote.player_one.id, vote.player_two.id):
        await interaction.followup.send(
            embed=make_embed(
                "Invalid Winner",
                "The winner must be one of the two players from that vote.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    scores, old_score, new_score, prestige_score = add_vote_prestige_to_winner(vote, winner)
    vote.confirmed = True

    if vote.message:
        await vote.message.edit(
            embed=make_vote_embed(
                vote.player_one,
                vote.player_two,
                vote.votes_by_user,
                closed=True,
                match_id=match_id,
                confirmed=True,
            ),
            view=vote,
            allowed_mentions=discord.AllowedMentions.none(),
        )

    summary = (
        f"Winner: {winner.mention}\n"
        f"Added Prestige: **{prestige_score}**\n"
        f"Previous total: **{old_score}**\n"
        f"New total: **{new_score}**"
    )
    await interaction.followup.send(embed=make_leaderboard_embed(scores, summary))


@tree.command(name="close_vote", description="Close a vote early and register the winner's Prestige.")
async def close_vote(interaction: discord.Interaction, match_id: int, winner: discord.Member):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    vote = MATCH_VOTES.get(match_id)

    if not vote:
        await interaction.followup.send(
            embed=make_embed(
                "Match Not Found",
                f"I could not find match ID `{match_id}`. Votes only stay available while the bot is running.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if vote.closed:
        await interaction.followup.send(
            embed=make_embed(
                "Vote Already Closed",
                f"Match ID `{match_id}` is already closed. Use `/confirm_winner` instead.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if winner.id not in (vote.player_one.id, vote.player_two.id):
        await interaction.followup.send(
            embed=make_embed(
                "Invalid Winner",
                "The winner must be one of the two players from that vote.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    await vote.close_vote()
    scores, old_score, new_score, prestige_score = add_vote_prestige_to_winner(vote, winner)
    vote.confirmed = True

    if vote.message:
        await vote.message.edit(
            embed=make_vote_embed(
                vote.player_one,
                vote.player_two,
                vote.votes_by_user,
                closed=True,
                match_id=match_id,
                confirmed=True,
            ),
            view=vote,
            allowed_mentions=discord.AllowedMentions.none(),
        )

    summary = (
        f"Vote closed early.\n"
        f"Winner: {winner.mention}\n"
        f"Added Prestige: **{prestige_score}**\n"
        f"Previous total: **{old_score}**\n"
        f"New total: **{new_score}**"
    )
    await interaction.followup.send(
        embed=make_leaderboard_embed(scores, summary),
    )


@tree.command(name="show_leaderboard", description="Show the Prestige leaderboard.")
async def show_leaderboard(interaction: discord.Interaction):
    await interaction.response.send_message(embed=make_leaderboard_embed(load_scores()))


@tree.command(name="show_current_round", description="Show the current CFI Endgame matchup round.")
async def show_current_round(interaction: discord.Interaction):
    await interaction.response.defer()
    round_robin = load_round_robin()

    if not round_robin["current_pairings"]:
        await interaction.followup.send(
            embed=make_embed(
                "No Current Round",
                "No CFI Endgame matchups have been created yet.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    await interaction.followup.send(
        embed=make_matchups_embed(round_robin["round"], round_robin["current_pairings"])
    )


@tree.command(name="start_endgame_poll", description="Start a win probability poll for the current 10 CFI Endgame players.")
async def start_endgame_poll(interaction: discord.Interaction):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    round_robin = load_round_robin()
    player_ids = round_robin["current_players"]
    player_names = round_robin.get("player_names", {})

    if interaction.guild:
        changed_names = False

        for player_id in player_ids:
            if str(player_id) not in player_names and str(player_id).isdigit():
                member = interaction.guild.get_member(int(player_id))

                if member:
                    player_names[str(player_id)] = member.display_name
                    changed_names = True

        if changed_names:
            round_robin["player_names"] = player_names
            save_round_robin(round_robin)

    if len(player_ids) != 10:
        await interaction.followup.send(
            embed=make_embed(
                "No Player List",
                "Run `/create_matchups` first so I know which 10 players are in Endgame.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    view = EndgameProbabilityView(interaction.guild, player_ids, player_names)
    try:
        view.message = await interaction.channel.send(
            embed=make_endgame_probability_embed(interaction.guild, player_ids, view.votes_by_user, player_names),
            view=view,
            allowed_mentions=discord.AllowedMentions.none(),
        )
    except discord.Forbidden:
        await interaction.followup.send(
            embed=make_embed(
                "Missing Permission",
                "I cannot send the Endgame poll in this channel. Give me Send Messages and Embed Links.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    await interaction.followup.send("Endgame probability poll started.", ephemeral=True)


@tree.command(name="create_matchups", description="Create round-robin matchups for 10 players.")
async def create_matchups(
    interaction: discord.Interaction,
    player_1: discord.Member,
    player_2: discord.Member,
    player_3: discord.Member,
    player_4: discord.Member,
    player_5: discord.Member,
    player_6: discord.Member,
    player_7: discord.Member,
    player_8: discord.Member,
    player_9: discord.Member,
    player_10: discord.Member,
):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    players = [
        player_1,
        player_2,
        player_3,
        player_4,
        player_5,
        player_6,
        player_7,
        player_8,
        player_9,
        player_10,
    ]
    player_ids = [str(player.id) for player in players]
    player_names = {str(player.id): player.display_name for player in players}

    if len(set(player_ids)) != 10:
        await interaction.followup.send(
            embed=make_embed(
                "Duplicate Player",
                "Choose 10 different players.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    round_robin = load_round_robin()
    pairings = find_round_robin_pairings(player_ids, round_robin["played_pairs"])

    if not pairings:
        await interaction.followup.send(
            embed=make_embed(
                "No Matchups Available",
                "I could not create a full round without repeat opponents. Use `/reset_cfi_matchups` to start over.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    record_undo("create CFI matchups", round_robin=round_robin)
    round_robin["round"] += 1

    for player_one_id, player_two_id in pairings:
        round_robin["played_pairs"].append(pair_key(player_one_id, player_two_id))

    round_robin["current_players"] = player_ids
    round_robin["current_pairings"] = pairings
    round_robin["player_names"] = player_names
    save_round_robin(round_robin)

    await interaction.followup.send(
        embed=make_matchups_embed(round_robin["round"], pairings)
    )


@tree.command(name="reset_cfi_matchups", description="Reset saved CFI Endgame matchup history.")
async def reset_cfi_matchups(interaction: discord.Interaction):
    if not await require_command_role(interaction):
        return

    record_undo("reset CFI matchups", round_robin=load_round_robin())
    save_round_robin({"played_pairs": [], "round": 0, "current_players": [], "current_pairings": [], "player_names": {}})
    await interaction.response.send_message(
        embed=make_embed(
            "CFI Endgame Matchups Reset",
            "CFI Endgame matchup history has been cleared.",
            SUCCESS_COLOR,
        )
    )


@tree.command(name="statcard_set", description="Create or update a player's stat card.")
@discord.app_commands.autocomplete(clan=clan_autocomplete)
async def statcard_set(
    interaction: discord.Interaction,
    player: discord.Member,
    wins: int,
    losses: int,
    goals: int,
    event: str,
    clan: str,
):
    if not await require_command_role(interaction):
        return

    if clan not in CLANS:
        await interaction.response.send_message(
            embed=make_embed(
                "Invalid Clan",
                "Choose a clan from the autocomplete list.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if min(wins, losses, goals) < 0:
        await interaction.response.send_message(
            embed=make_embed(
                "Invalid Stats",
                "Wins, losses, and goals cannot be negative.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    event_name = event.strip()

    if not event_name:
        await interaction.response.send_message(
            embed=make_embed(
                "Invalid Event",
                "Event cannot be empty.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    statcards = load_statcards()
    record_undo("stat card change", statcards=statcards)
    stats = {
        "wins": wins,
        "losses": losses,
        "goals": goals,
        "event": event_name,
        "clan": clan,
    }
    statcards[str(player.id)] = stats
    save_statcards(statcards)

    await interaction.response.send_message(embed=make_statcard_embed(player, stats))


@tree.command(name="statcard_show", description="Show a player's stat card.")
async def statcard_show(interaction: discord.Interaction, player: discord.Member):
    statcards = load_statcards()
    stats = statcards.get(str(player.id))

    if not stats:
        await interaction.response.send_message(
            embed=make_embed(
                "Stat Card Not Found",
                f"No stat card exists for {player.mention} yet.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    await interaction.response.send_message(embed=make_statcard_embed(player, stats))


@tree.command(name="profile", description="Show a player's tournament profile.")
async def profile(interaction: discord.Interaction, player: discord.Member = None):
    target = player or interaction.user
    profiles = load_profiles()
    profile_data = get_profile(profiles, target.id)
    await interaction.response.send_message(embed=make_profile_embed(target, profile_data))


@tree.command(name="show_profile", description="Show your tournament profile or another player's profile.")
async def show_profile(interaction: discord.Interaction, player: discord.Member = None):
    target = player or interaction.user
    profiles = load_profiles()
    profile_data = get_profile(profiles, target.id)
    await interaction.response.send_message(embed=make_profile_embed(target, profile_data))


def is_valid_profile_url(url):
    if not url:
        return True

    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_direct_media_url(url):
    parsed = urllib.parse.urlparse(url)
    hostname = (parsed.hostname or "").lower()
    path = parsed.path.lower()

    if path.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
        return True

    direct_media_hosts = (
        "cdn.discordapp.com",
        "media.discordapp.net",
        "media.tenor.com",
        "tenor.com",
        "media.giphy.com",
        "i.giphy.com",
    )

    return hostname in direct_media_hosts or hostname.endswith(".discordapp.net")


def is_resolvable_media_page(url):
    hostname = (urllib.parse.urlparse(url).hostname or "").lower()
    return hostname in {"tenor.com", "www.tenor.com", "giphy.com", "www.giphy.com"}


def extract_meta_image(html_text):
    patterns = [
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image["\']',
    ]

    for pattern in patterns:
        match = re.search(pattern, html_text, flags=re.IGNORECASE)

        if match:
            return html.unescape(match.group(1))

    return None


def resolve_profile_media_url(url):
    if not url:
        return ""

    if is_direct_media_url(url) and not is_resolvable_media_page(url):
        return url

    if not is_resolvable_media_page(url):
        return url

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": CHALLONGE_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            html_text = response.read(1_000_000).decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError):
        return url

    media_url = extract_meta_image(html_text)
    return media_url or url


@tree.command(name="edit_profile", description="Edit your public profile clan and link.")
@discord.app_commands.autocomplete(clan=clan_autocomplete, country=country_autocomplete)
async def edit_profile(interaction: discord.Interaction, clan: str, country: str = "", url: str = ""):
    if clan not in CLANS:
        await interaction.response.send_message(
            embed=make_embed("Invalid Clan", "Choose a clan from the autocomplete list.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    clean_url = url.strip()
    should_update_url = bool(clean_url)
    country_name, country_code = normalize_country(country)

    if country_name is None:
        await interaction.response.send_message(
            embed=make_embed("Invalid Country", "Choose a country from the autocomplete list, use a 2-letter country code, or type `None`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if clean_url.lower() in {"none", "clear", "remove"}:
        clean_url = ""

    if should_update_url and len(clean_url) > 1000:
        await interaction.response.send_message(
            embed=make_embed("URL Too Long", "Keep the profile URL under 1000 characters.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if should_update_url and clean_url and not is_valid_profile_url(clean_url):
        await interaction.response.send_message(
            embed=make_embed("Invalid URL", "Use a full link starting with `https://` or `http://`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if should_update_url and clean_url:
        clean_url = await asyncio.to_thread(resolve_profile_media_url, clean_url)

    if should_update_url and clean_url and not is_direct_media_url(clean_url):
        await interaction.response.send_message(
            embed=make_embed(
                "Direct Image Needed",
                "Use a Discord GIF/image link, Tenor GIF, Giphy link, or direct `.png`, `.jpg`, `.gif`, or `.webp` URL.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    profiles = load_profiles()
    profile_data = get_profile(profiles, interaction.user.id)
    profile_data["clan"] = clan

    if country.strip():
        profile_data["country"] = country_name
        profile_data["country_code"] = country_code

    if should_update_url:
        profile_data["url"] = clean_url

    save_profiles(profiles)

    await interaction.response.send_message(
        embed=make_profile_embed(interaction.user, profile_data),
        ephemeral=True,
    )


@tree.command(name="admin_edit_profile", description="Organiser: adjust another player's profile stats.")
@discord.app_commands.autocomplete(clan=clan_autocomplete, country=country_autocomplete)
async def admin_edit_profile(
    interaction: discord.Interaction,
    player: discord.Member,
    prestige: int = -1,
    wins: int = -1,
    losses: int = -1,
    goals_for: int = -1,
    goals_against: int = -1,
    arch_nemesis: discord.Member = None,
    clan: str = "",
    country: str = "",
    url: str = "",
):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    clean_clan = clan.strip()

    if clean_clan and clean_clan not in CLANS:
        await interaction.followup.send(
            embed=make_embed("Invalid Clan", "Choose a clan from the autocomplete list.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    country_name = ""
    country_code = ""

    if country.strip():
        country_name, country_code = normalize_country(country)

        if country_name is None:
            await interaction.followup.send(
                embed=make_embed(
                    "Invalid Country",
                    "Choose a country from the autocomplete list, use a 2-letter country code, or type `None`.",
                    ERROR_COLOR,
                ),
                ephemeral=True,
            )
            return

    clean_url = url.strip()
    should_update_url = bool(clean_url)

    if clean_url.lower() in {"none", "clear", "remove"}:
        clean_url = ""

    if should_update_url and len(clean_url) > 1000:
        await interaction.followup.send(
            embed=make_embed("URL Too Long", "Keep the profile URL under 1000 characters.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if should_update_url and clean_url and not is_valid_profile_url(clean_url):
        await interaction.followup.send(
            embed=make_embed("Invalid URL", "Use a full link starting with `https://` or `http://`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if should_update_url and clean_url:
        clean_url = await asyncio.to_thread(resolve_profile_media_url, clean_url)

    if should_update_url and clean_url and not is_direct_media_url(clean_url):
        await interaction.followup.send(
            embed=make_embed(
                "Direct Image Needed",
                "Use a Discord GIF/image link, Tenor GIF, Giphy link, or direct `.png`, `.jpg`, `.gif`, or `.webp` URL.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    numeric_updates = {
        "prestige": prestige,
        "wins": wins,
        "losses": losses,
        "goals_for": goals_for,
        "goals_against": goals_against,
    }

    for label, value in numeric_updates.items():
        if value < -1:
            await interaction.followup.send(
                embed=make_embed("Invalid Value", f"`{label}` must be `0` or higher, or left empty.", ERROR_COLOR),
                ephemeral=True,
            )
            return

    profiles = load_profiles()
    record_undo("admin edit profile", profiles=profiles)
    profile_data = get_profile(profiles, player.id)

    for key, value in numeric_updates.items():
        if value >= 0:
            profile_data[key] = value

    if arch_nemesis:
        profile_data["last_lost_to"] = str(arch_nemesis.id)
        profile_data["last_lost_to_name"] = arch_nemesis.display_name

    if clean_clan:
        profile_data["clan"] = clean_clan

    if country.strip():
        profile_data["country"] = country_name
        profile_data["country_code"] = country_code

    if should_update_url:
        profile_data["url"] = clean_url

    save_profiles(profiles)

    await interaction.followup.send(
        embed=make_profile_embed(player, profile_data),
        ephemeral=True,
    )


@tree.command(name="score_reset_player", description="Remove one player from the leaderboard.")
async def score_reset_player(interaction: discord.Interaction, player: discord.Member):
    if not await require_command_role(interaction):
        return

    player_id = str(player.id)
    scores = load_scores()

    if player_id not in scores:
        await interaction.response.send_message(
            embed=make_embed("Player Not Found", f"Could not find {player.mention}.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("remove leaderboard player", scores=scores)
    del scores[player_id]
    save_scores(scores)
    await interaction.response.send_message(
        embed=make_leaderboard_embed(scores, f"Removed {player.mention} from the leaderboard.")
    )


@tree.command(name="score_reset_all", description="Clear the whole leaderboard.")
async def score_reset_all(interaction: discord.Interaction):
    if not await require_command_role(interaction):
        return

    record_undo("reset leaderboard", scores=load_scores())
    save_scores({})
    await interaction.response.send_message(
        embed=make_embed("Leaderboard Cleared", "All scores have been removed.", SUCCESS_COLOR)
    )


@tree.command(name="reset_leaderboard", description="Reset the Prestige leaderboard completely.")
async def reset_leaderboard(interaction: discord.Interaction):
    if not await require_command_role(interaction):
        return

    record_undo("reset leaderboard", scores=load_scores())
    save_scores({})
    await interaction.response.send_message(
        embed=make_embed("Leaderboard Reset", "The Prestige leaderboard has been cleared.", SUCCESS_COLOR)
    )


@tree.command(name="tournament_create", description="Create a new local tournament.")
async def tournament_create(
    interaction: discord.Interaction,
    name: str,
    start_time: str,
    inscriptions_channel: TournamentPostChannel,
    results_channel: TournamentPostChannel,
    profiles_channel: TournamentPostChannel,
):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    for selected_channel in (inscriptions_channel, results_channel, profiles_channel):
        if not is_tournament_post_channel(selected_channel):
            await interaction.followup.send(embed=invalid_tournament_channel_embed(selected_channel), ephemeral=True)
            return

    tournaments = load_tournaments()
    active_tournament = get_active_tournament(tournaments, interaction.guild)

    if active_tournament and active_tournament.get("status") != "completed":
        await interaction.followup.send(
            embed=make_embed(
                "Tournament Already Active",
                "Reset or finish the current tournament before creating another one.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    record_undo("create tournament", tournaments=tournaments)

    tournament_id = str(tournaments.get("next_id", 1))
    tournaments["next_id"] = int(tournament_id) + 1
    set_active_tournament(tournaments, interaction.guild, tournament_id)
    tournaments["tournaments"][tournament_id] = {
        "id": tournament_id,
        "guild_id": str(interaction.guild_id),
        "name": name,
        "start_time": start_time.strip(),
        "status": "setup",
        "players": [],
        "rounds": [],
        "current_round": 0,
        "winner": None,
        "challonge": {},
        "messages": {},
        "channels": {
            "inscriptions": str(inscriptions_channel.id),
            "results": str(results_channel.id),
            "profiles": str(profiles_channel.id),
            "round_control": str(inscriptions_channel.id),
        },
    }
    tournament = tournaments["tournaments"][tournament_id]
    await upsert_tournament_control_center(interaction.guild, tournament)
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed(
            "Tournament Created",
            (
                f"Control center: {inscriptions_channel.mention}\n"
                f"Results: {results_channel.mention}\n"
                f"Profiles: {profiles_channel.mention}\n"
                "Round control will replace the registration hub when the tournament starts."
            ),
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="tournament_add", description="Add one or more players to the active tournament.")
async def tournament_add(
    interaction: discord.Interaction,
    player: discord.Member,
    player2: discord.Member = None,
    player3: discord.Member = None,
    player4: discord.Member = None,
    player5: discord.Member = None,
    player6: discord.Member = None,
    player7: discord.Member = None,
    player8: discord.Member = None,
    player9: discord.Member = None,
    player10: discord.Member = None,
):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "Create one first with `/tournament_create`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("status") != "setup":
        await interaction.followup.send(
            embed=make_embed(
                "Tournament Already Started",
                "Players can only be added before the bracket starts.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    selected_players = [
        selected_player
        for selected_player in (player, player2, player3, player4, player5, player6, player7, player8, player9, player10)
        if selected_player
    ]
    unique_players = []
    seen_ids = set()
    duplicate_mentions = []

    for selected_player in selected_players:
        player_id = str(selected_player.id)

        if player_id in seen_ids:
            duplicate_mentions.append(selected_player.mention)
            continue

        seen_ids.add(player_id)
        unique_players.append(selected_player)

    existing_ids = {str(existing_player["id"]) for existing_player in tournament["players"]}
    players_to_add = [
        selected_player
        for selected_player in unique_players
        if str(selected_player.id) not in existing_ids
    ]
    already_added_mentions = [
        selected_player.mention
        for selected_player in unique_players
        if str(selected_player.id) in existing_ids
    ]

    if not players_to_add:
        await interaction.followup.send(
            embed=make_embed(
                "No Players Added",
                "Everyone selected is already in this tournament.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    record_undo("add tournament players", tournaments=tournaments)
    added_players = []

    for selected_player in players_to_add:
        add_member_to_tournament(tournament, selected_player)
        added_players.append(tournament["players"][-1])

    challonge_sync = None
    challonge_errors = []

    try:
        if not tournament.get("challonge_url"):
            challonge_sync = await ensure_setup_challonge_bracket(tournament)
        else:
            for added_player in added_players:
                try:
                    await sync_new_player_to_challonge(tournament, added_player)
                except RuntimeError as error:
                    challonge_errors.append(f"{tournament_player_label(added_player)}: {error}")
    except RuntimeError as error:
        challonge_errors.append(str(error))

    await upsert_tournament_control_center(interaction.guild, tournament)
    save_tournaments(tournaments)

    added_mentions = ", ".join(selected_player.mention for selected_player in players_to_add)
    summary_lines = [f"Added **{len(players_to_add)}** player(s): {added_mentions}"]

    if already_added_mentions:
        summary_lines.append(f"Already registered: {', '.join(already_added_mentions)}")

    if duplicate_mentions:
        summary_lines.append(f"Duplicate selections ignored: {', '.join(duplicate_mentions)}")

    if isinstance(challonge_sync, tuple) and challonge_sync[0] == "created":
        summary_lines.append(f"Challonge created: {challonge_sync[1]}")

    if challonge_errors:
        summary_lines.append("Challonge warnings:\n" + "\n".join(challonge_errors[:5]))

    if challonge_errors:
        await interaction.followup.send(
            embed=make_embed(
                "Players Added Locally",
                "\n".join(summary_lines)[:3900],
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
    else:
        await interaction.followup.send(
            embed=make_embed("Players Added", "\n".join(summary_lines)[:3900], SUCCESS_COLOR),
            ephemeral=True,
        )


@tree.command(name="set_tournament_role", description="Set the role given by the tournament hub Join button.")
async def set_tournament_role(interaction: discord.Interaction, role: discord.Role):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    if not interaction.guild:
        await interaction.followup.send(
            embed=make_embed("Server Only", "This command can only be used inside a server.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "Create one first with `/tournament_create`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("status") != "setup":
        await interaction.followup.send(
            embed=make_embed(
                "Tournament Already Started",
                "The tournament role can only be changed during registration.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if role.is_default() or role.managed:
        await interaction.followup.send(
            embed=make_embed("Invalid Role", "Choose a normal role that the bot can assign.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    bot_member = interaction.guild.me or interaction.guild.get_member(client.user.id)

    if not bot_member or not bot_member.guild_permissions.manage_roles:
        await interaction.followup.send(
            embed=make_embed(
                "Missing Permission",
                "I need the **Manage Roles** permission before I can give people the tournament role.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if role >= bot_member.top_role:
        await interaction.followup.send(
            embed=make_embed(
                "Role Too High",
                "Move my bot role above the role you want me to give, then try again.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    record_undo("set tournament registration role", tournaments=tournaments)
    registration = tournament.setdefault("registration", {})
    registration["role_id"] = str(role.id)
    registration.setdefault("message", "Press the button below if you want to join the tournament.")

    await upsert_tournament_control_center(interaction.guild, tournament)
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed(
            "Tournament Role Saved",
            (
                f"The hub **Join Tournament** button will now give {role.mention} when players register.\n\n"
                "If your current hub message is old, run `/tournament_hub_repost` once so it has the newest buttons."
            ),
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


async def validate_assignable_tournament_role(interaction: discord.Interaction, role: discord.Role, purpose="registration role"):
    if role.is_default() or role.managed:
        await interaction.followup.send(
            embed=make_embed("Invalid Role", "Choose a normal role that the bot can assign.", ERROR_COLOR),
            ephemeral=True,
        )
        return False

    bot_member = interaction.guild.me or interaction.guild.get_member(client.user.id)

    if not bot_member or not bot_member.guild_permissions.manage_roles:
        await interaction.followup.send(
            embed=make_embed(
                "Missing Permission",
                f"I need the **Manage Roles** permission before I can give people the {purpose}.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return False

    if role >= bot_member.top_role:
        await interaction.followup.send(
            embed=make_embed(
                "Role Too High",
                "Move my bot role above the role you want me to give, then try again.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return False

    return True


@tree.command(name="register", description="DM server members a tournament registration invite.")
async def register(
    interaction: discord.Interaction,
    role: discord.Role,
    message: str = "Press the button below if you want to join the tournament.",
):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not interaction.guild:
        await interaction.followup.send(
            embed=make_embed("Server Only", "This command can only be used inside a server.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    is_server_owner = interaction.guild.owner_id == interaction.user.id
    has_server_permission = (
        isinstance(interaction.user, discord.Member)
        and (
            interaction.user.guild_permissions.administrator
            or interaction.user.guild_permissions.manage_guild
            or interaction.user.guild_permissions.manage_roles
        )
    )

    if not is_server_owner and not has_server_permission:
        await interaction.followup.send(
            embed=make_embed(
                "Missing Permission",
                "You need Administrator, Manage Server, or Manage Roles to send tournament registration DMs.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "Create one first with `/tournament_create`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("status") != "setup":
        await interaction.followup.send(
            embed=make_embed(
                "Tournament Already Started",
                "Registration DMs can only be sent before the bracket starts.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if not await validate_assignable_tournament_role(interaction, role):
        return

    record_undo("start tournament registration", tournaments=tournaments)
    tournament["registration"] = {
        "role_id": str(role.id),
        "message": message,
    }
    challonge_status = None

    if not tournament.get("challonge_url"):
        try:
            challonge_sync = await ensure_setup_challonge_bracket(tournament)

            if isinstance(challonge_sync, tuple) and challonge_sync[0] == "created":
                _, challonge_url, participant_count = challonge_sync
                challonge_status = f"Challonge bracket created immediately: {challonge_url}\nPlayers synced now: **{participant_count}**"
            elif challonge_sync == "waiting_for_players":
                challonge_status = "Challonge will auto-create once at least 2 players are registered."
            elif challonge_sync == "missing_key":
                challonge_status = "Challonge auto-create is disabled because the API key is missing."
        except RuntimeError as error:
            challonge_status = f"Challonge auto-create failed: {error}"

    await upsert_tournament_control_center(interaction.guild, tournament)
    save_tournaments(tournaments)

    asyncio.create_task(
        send_registration_invites_background(
            interaction.guild.id,
            role.id,
            tournament["id"],
            message,
            report_channel_id=interaction.channel_id,
        )
    )

    await interaction.followup.send(
        embed=make_embed(
            "Registration DMs Started",
            (
                "I started sending the tournament invite in the background.\n"
                "This can take a while on large servers, and I will post a summary when it finishes.\n\n"
                "People who click the DM button will receive the role and be added to the active tournament."
                + (f"\n\n{challonge_status}" if challonge_status else "")
            ),
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="registration_hub", description="Post a clean registration hub with buttons and no player list.")
async def registration_hub(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    role: discord.Role = None,
    message: str = "Press the button below if you want to join the tournament.",
):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    if not interaction.guild:
        await interaction.followup.send(
            embed=make_embed("Server Only", "This command can only be used inside a server.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "Create one first with `/tournament_create`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("status") != "setup":
        await interaction.followup.send(
            embed=make_embed(
                "Tournament Already Started",
                "The public registration hub can only be posted while registration is open.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    registration = tournament.setdefault("registration", {})
    saved_role_id = registration.get("role_id")

    if role is None and saved_role_id:
        role = interaction.guild.get_role(int(saved_role_id))

    if role is None:
        await interaction.followup.send(
            embed=make_embed(
                "Role Needed",
                "Choose the tournament entry role in this command, or set it first with `/set_tournament_role`.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if not await validate_assignable_tournament_role(interaction, role):
        return

    if len(message) > 1500:
        await interaction.followup.send(
            embed=make_embed("Message Too Long", "Keep the registration hub message under 1500 characters.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("post public registration hub", tournaments=tournaments)
    registration["role_id"] = str(role.id)
    registration["message"] = message

    embed = make_tournament_registration_embed(interaction.guild, tournament, role, message, include_invite_image=True)
    view = TournamentRegistrationView(interaction.guild.id, role.id, tournament["id"])
    file = make_tournament_registration_file()

    try:
        if file:
            await channel.send(embed=embed, view=view, file=file)
        else:
            await channel.send(embed=embed, view=view)
    except discord.Forbidden:
        await interaction.followup.send(
            embed=make_embed(
                "Cannot Post Hub",
                f"I do not have permission to send messages in {channel.mention}.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return
    except discord.HTTPException as exc:
        await interaction.followup.send(
            embed=make_embed("Cannot Post Hub", f"Discord rejected the hub message: {exc}", ERROR_COLOR),
            ephemeral=True,
        )
        return

    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed(
            "Registration Hub Posted",
            f"Posted a clean registration hub in {channel.mention}. Players can register from that button.",
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="tournament_remove", description="Remove a player from the active tournament before it starts.")
async def tournament_remove(interaction: discord.Interaction, player: discord.Member):
    await remove_tournament_player(interaction, player, command_name="remove tournament player")


@tree.command(name="register_dm", description="DM a slow, limited batch of tournament invites.")
async def register_dm(
    interaction: discord.Interaction,
    tournament_role: discord.Role,
    message: str = "Press the button below if you want to join the tournament.",
    target_role: discord.Role = None,
    limit: int = 25,
):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    if not interaction.guild:
        await interaction.followup.send(
            embed=make_embed("Server Only", "This command can only be used inside a server.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament_role.is_default() or tournament_role.managed:
        await interaction.followup.send(
            embed=make_embed("Invalid Role", "Choose a normal tournament role that the bot can assign.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    bot_member = interaction.guild.me or interaction.guild.get_member(client.user.id)

    if not bot_member or not bot_member.guild_permissions.manage_roles:
        await interaction.followup.send(
            embed=make_embed(
                "Missing Permission",
                "I need the **Manage Roles** permission before I can give people the tournament role.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if tournament_role >= bot_member.top_role:
        await interaction.followup.send(
            embed=make_embed(
                "Role Too High",
                "Move my bot role above the tournament role, then try again.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    limit = max(1, min(int(limit or 25), 50))
    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "Create one first with `/tournament_create`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("status") != "setup":
        await interaction.followup.send(
            embed=make_embed(
                "Tournament Already Started",
                "Registration DMs can only be sent before the bracket starts.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    record_undo("send tournament registration dm batch", tournaments=tournaments)
    registration = tournament.setdefault("registration", {})
    registration["role_id"] = str(tournament_role.id)
    registration["message"] = message
    invited_ids = set(str(player_id) for player_id in registration.setdefault("dm_invited_ids", []))
    failed_ids = set(str(player_id) for player_id in registration.setdefault("dm_failed_ids", []))
    save_tournaments(tournaments)

    embed = make_tournament_registration_embed(interaction.guild, tournament, tournament_role, message, include_invite_image=False)
    view = TournamentRegistrationView(interaction.guild.id, tournament_role.id, tournament["id"])
    sent_count = 0
    failed_count = 0
    skipped_count = 0
    failure_reasons = {}

    def count_failure(reason):
        failure_reasons[reason] = failure_reasons.get(reason, 0) + 1

    try:
        members = [member async for member in interaction.guild.fetch_members(limit=None)]
    except discord.HTTPException:
        members = list(interaction.guild.members)

    for member in members:
        member_id = str(member.id)

        if sent_count >= limit:
            break

        if member.bot:
            skipped_count += 1
            continue

        if target_role and target_role not in member.roles:
            skipped_count += 1
            continue

        if member_id in invited_ids or member_id in failed_ids:
            skipped_count += 1
            continue

        try:
            await member.send(
                content=f"{member.mention} \u26A1 your tournament invitation is here.",
                embed=embed,
                view=view,
                allowed_mentions=discord.AllowedMentions(users=True),
            )
            sent_count += 1
            invited_ids.add(member_id)
        except discord.Forbidden as error:
            failed_count += 1
            failed_ids.add(member_id)
            count_failure(f"Forbidden {getattr(error, 'status', 403)}")
        except discord.HTTPException as error:
            failed_count += 1
            failed_ids.add(member_id)
            count_failure(f"HTTP {getattr(error, 'status', 'unknown')} code {getattr(error, 'code', 'unknown')}")
        except OSError as error:
            failed_count += 1
            count_failure(f"Network/File error {getattr(error, 'errno', 'unknown')}")

        await asyncio.sleep(random.uniform(6, 14))

    registration["dm_invited_ids"] = sorted(invited_ids)
    registration["dm_failed_ids"] = sorted(failed_ids)
    await upsert_tournament_control_center(interaction.guild, tournament)
    save_tournaments(tournaments)

    reason_lines = [
        f"- {reason}: **{count}**"
        for reason, count in sorted(failure_reasons.items(), key=lambda item: item[1], reverse=True)[:5]
    ]
    target_text = f"\nTarget role: {target_role.mention}" if target_role else "\nTarget: all non-bot members not already tried"

    await interaction.followup.send(
        embed=make_embed(
            "Registration DM Batch Finished",
            (
                f"Sent: **{sent_count}**\n"
                f"Failed: **{failed_count}**\n"
                f"Skipped: **{skipped_count}**"
                f"{target_text}\n\n"
                "Run this command again later to continue with the next untried batch."
                + (f"\n\nFailure reasons:\n" + "\n".join(reason_lines) if reason_lines else "")
            ),
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="register_dm_test", description="Test whether the bot can DM one member.")
async def register_dm_test(interaction: discord.Interaction, player: discord.Member):
    if not await safe_defer(interaction, ephemeral=True):
        return

    try:
        await player.send(
            content=f"{player.mention} \u26A1 test tournament invite DM.",
            allowed_mentions=discord.AllowedMentions(users=True),
        )
    except discord.Forbidden as error:
        await interaction.followup.send(
            embed=make_embed(
                "DM Test Failed",
                (
                    f"Discord refused the DM to {player.mention}.\n"
                    f"Reason: **Forbidden {getattr(error, 'status', 403)}**\n\n"
                    "That means private DM invites cannot reach this user. Use public registration pings instead."
                ),
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return
    except discord.HTTPException as error:
        await interaction.followup.send(
            embed=make_embed(
                "DM Test Failed",
                f"Discord returned HTTP **{getattr(error, 'status', 'unknown')}** code **{getattr(error, 'code', 'unknown')}**.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    await interaction.followup.send(
        embed=make_embed("DM Test Sent", f"The bot successfully DMed {player.mention}.", SUCCESS_COLOR),
        ephemeral=True,
    )


@tree.command(name="tournament_start", description="Start the active tournament bracket.")
async def tournament_start(interaction: discord.Interaction, shuffle_players: bool = False):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "Create one first with `/tournament_create`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("status") != "setup":
        await interaction.followup.send(
            embed=make_embed("Already Started", "This tournament bracket has already started.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if len(tournament.get("players", [])) < 2:
        await interaction.followup.send(
            embed=make_embed("Not Enough Players", "Add at least 2 players before starting.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("start tournament", tournaments=tournaments)
    start_tournament_bracket(tournament, shuffle_players=shuffle_players)
    await upsert_tournament_control_center(interaction.guild, tournament)
    await upsert_round_control_center(interaction.guild, tournament)
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed("Tournament Started", "The control center and round control have been updated.", SUCCESS_COLOR),
        ephemeral=True,
    )


@tree.command(name="tournament_show", description="Show the active tournament bracket.")
async def tournament_show(interaction: discord.Interaction):
    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.response.send_message(
            embed=make_embed("No Tournament", "No active tournament has been created yet.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    await interaction.response.send_message(embed=make_tournament_embed(tournament, interaction.guild))


@tree.command(name="participants", description="Show the registered players for the active tournament.")
async def participants(interaction: discord.Interaction):
    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.response.send_message(
            embed=make_embed("No Tournament", "No active tournament has been created yet.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    await interaction.response.send_message(embed=make_participants_embed(tournament, interaction.guild))


@tree.command(name="participants_export", description="Export the full registered player list as a text file.")
async def participants_export(interaction: discord.Interaction):
    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.response.send_message(
            embed=make_embed("No Tournament", "No active tournament has been created yet.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    players = tournament.get("players", [])
    lines = [
        f"{index}. {tournament_player_label(player, interaction.guild)} | ID: {player.get('id', 'unknown')}"
        for index, player in enumerate(players, start=1)
    ]
    text = "\n".join(lines) if lines else "No players registered yet."
    data = io.BytesIO(text.encode("utf-8"))
    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", tournament.get("name", "tournament")).strip("_") or "tournament"
    file = discord.File(data, filename=f"{safe_name}_participants.txt")

    await interaction.response.send_message(
        embed=make_embed("Participants Export", f"Exported **{len(players)}** registered players.", SUCCESS_COLOR),
        file=file,
        ephemeral=True,
    )


@tree.command(name="match", description="Show your current tournament match.")
async def match(interaction: discord.Interaction):
    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.response.send_message(
            embed=make_embed("No Tournament", "No active tournament has been created yet.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("status") == "setup":
        is_registered = any(str(player.get("id")) == str(interaction.user.id) for player in tournament.get("players", []))
        message = "You are registered. The bracket has not started yet." if is_registered else "You are not registered for this tournament."
        await interaction.response.send_message(
            embed=make_embed("No Match Yet", message, EMBED_COLOR),
            ephemeral=True,
        )
        return

    player_match = find_any_tournament_match_by_player(tournament, interaction.user.id)

    if not player_match:
        await interaction.response.send_message(
            embed=make_embed("Match Not Found", "I could not find you in the current tournament bracket.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    opponent = player_match.get("player_two")

    if str(player_match.get("player_two", {}).get("id")) == str(interaction.user.id):
        opponent = player_match.get("player_one")

    state = str(player_match.get("state", "open")).title()
    score = player_match.get("score")
    score_text = ""

    if isinstance(score, dict):
        score_text = f"\nScore: **{score.get('player_one', 0)}-{score.get('player_two', 0)}**"

    await interaction.response.send_message(
        embed=make_embed(
            "Your Tournament Match",
            (
                f"Tournament: **{tournament['name']}**\n"
                f"Round: **{player_match.get('round')}**\n"
                f"Opponent: {tournament_player_label(opponent, interaction.guild)}\n"
                f"Status: **{state}**{score_text}"
            ),
            EMBED_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="admin_panel", description="Show the active tournament control overview.")
async def admin_panel(interaction: discord.Interaction):
    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.response.send_message(
            embed=make_embed("No Tournament", "No active tournament has been created yet.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    await interaction.response.send_message(embed=make_admin_panel_embed(interaction.guild, tournament), ephemeral=True)


@tree.command(name="tournament_channels", description="Change where tournament channels are posted.")
async def tournament_channels(
    interaction: discord.Interaction,
    inscriptions_channel: TournamentPostChannel,
    results_channel: TournamentPostChannel,
    profiles_channel: TournamentPostChannel,
):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    for selected_channel in (inscriptions_channel, results_channel, profiles_channel):
        if not is_tournament_post_channel(selected_channel):
            await interaction.followup.send(embed=invalid_tournament_channel_embed(selected_channel), ephemeral=True)
            return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "No active tournament has been created yet.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("change tournament channels", tournaments=tournaments)
    tournament["channels"] = {
        "inscriptions": str(inscriptions_channel.id),
        "results": str(results_channel.id),
        "profiles": str(profiles_channel.id),
        "round_control": str(inscriptions_channel.id),
    }
    await upsert_tournament_control_center(interaction.guild, tournament)
    await upsert_round_control_center(interaction.guild, tournament)
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed(
            "Tournament Channels Updated",
            (
                f"Inscriptions: {inscriptions_channel.mention}\n"
                f"Results: {results_channel.mention}\n"
                f"Profiles: {profiles_channel.mention}\n"
                "Round control will replace the registration hub when the tournament starts."
            ),
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="tournament_hub_repost", description="Repost the active tournament hub fresh in the inscriptions channel.")
async def tournament_hub_repost(interaction: discord.Interaction):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "No active tournament has been created yet.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    channel = get_tournament_channel(interaction.guild, tournament, "inscriptions")

    if not channel:
        await interaction.followup.send(
            embed=make_embed("No Inscriptions Channel", "Set an inscriptions channel with `/tournament_channels` first.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("repost tournament hub", tournaments=tournaments)
    messages = tournament.setdefault("messages", {})
    messages.pop("control_center", None)
    await upsert_tournament_control_center(interaction.guild, tournament)
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed("Tournament Hub Reposted", f"Posted a fresh hub in {channel.mention}.", SUCCESS_COLOR),
        ephemeral=True,
    )


async def remove_tournament_player(interaction, player, command_name="drop"):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "There is no active tournament to edit.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("status") != "setup":
        await interaction.followup.send(
            embed=make_embed(
                "Tournament Already Started",
                "Players can only be removed before the bracket starts. Use `/dq` after the tournament starts.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    old_count = len(tournament["players"])
    updated_players = [
        existing_player
        for existing_player in tournament["players"]
        if existing_player["id"] != str(player.id)
    ]

    if len(updated_players) == old_count:
        await interaction.followup.send(
            embed=make_embed("Player Not Found", f"{player.mention} is not in this tournament.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo(f"{command_name} tournament player", tournaments=tournaments)
    challonge_warning = None

    if tournament.get("challonge_url") and CHALLONGE_API_KEY:
        try:
            challonge_warning = await sync_removed_player_from_challonge(tournament, player.id)
        except RuntimeError as error:
            challonge_warning = str(error)

    tournament["players"] = updated_players
    await upsert_tournament_control_center(interaction.guild, tournament)
    save_tournaments(tournaments)
    note = f"{player.mention} was removed from the control center."

    if challonge_warning:
        note += f"\n\nChallonge warning: {challonge_warning}"
    elif tournament.get("challonge_url") and CHALLONGE_API_KEY:
        note += "\n\nChallonge participant removed too."

    await interaction.followup.send(
        embed=make_embed("Player Dropped", note, SUCCESS_COLOR),
        ephemeral=True,
    )


@tree.command(name="drop", description="Drop a player from the tournament before it starts.")
async def drop(interaction: discord.Interaction, player: discord.Member):
    await remove_tournament_player(interaction, player, command_name="drop")


def normalize_challonge_url(url):
    clean_url = url.strip()
    parsed = urllib.parse.urlparse(clean_url)

    if not parsed.scheme:
        clean_url = f"https://{clean_url}"
        parsed = urllib.parse.urlparse(clean_url)

    hostname = (parsed.hostname or "").lower()

    if hostname not in {"challonge.com", "www.challonge.com"}:
        return None

    path_parts = [part for part in parsed.path.split("/") if part]

    if not path_parts:
        return None

    return urllib.parse.urlunparse(("https", "challonge.com", "/" + "/".join(path_parts), "", "", ""))


@tree.command(name="challonge_status", description="Check the linked Challonge bracket.")
async def challonge_status(interaction: discord.Interaction):
    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)
    linked_status = "No active local tournament."
    api_key_status = "Configured" if CHALLONGE_API_KEY else "Missing"

    if tournament:
        linked_status = tournament.get("challonge_url") or "No Challonge bracket linked yet."

    await interaction.response.send_message(
        embed=make_embed(
            "Challonge Status",
            (
                f"API v1 key: **{api_key_status}**\n"
                f"Active tournament link:\n{linked_status}"
            ),
            SUCCESS_COLOR if CHALLONGE_API_KEY else ERROR_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="challonge_link", description="Link a manually created Challonge bracket to the active tournament.")
async def challonge_link(interaction: discord.Interaction, url: str):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    normalized_url = normalize_challonge_url(url)

    if not normalized_url:
        await interaction.followup.send(
            embed=make_embed(
                "Invalid Challonge Link",
                "Paste the full Challonge tournament link, like `https://challonge.com/your-bracket`.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "Create one first with `/tournament_create`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("link Challonge tournament", tournaments=tournaments)
    tournament["challonge"] = {
        "mode": "manual_link",
        "url": normalized_url,
    }
    tournament["challonge_url"] = normalized_url
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed(
            "Challonge Bracket Linked",
            (
                f"Linked **{tournament['name']}** to Challonge.\n"
                f"{normalized_url}\n\n"
                "`/tournament_show` will now display the bracket link."
            ),
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="challonge_unlink", description="Remove the Challonge link from the active tournament.")
async def challonge_unlink(interaction: discord.Interaction):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "No active tournament has been created yet.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if not tournament.get("challonge_url"):
        await interaction.followup.send(
            embed=make_embed("No Challonge Link", "This tournament does not have a Challonge link saved.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("unlink Challonge tournament", tournaments=tournaments)
    tournament["challonge"] = {}
    tournament.pop("challonge_url", None)
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed("Challonge Link Removed", "The active tournament is no longer linked to Challonge.", SUCCESS_COLOR),
        ephemeral=True,
    )


@tree.command(name="challonge_create", description="Create a Challonge bracket from the active tournament using the API v1 key.")
async def challonge_create(
    interaction: discord.Interaction,
    private: bool = False,
    url_slug: str = "",
):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    if not CHALLONGE_API_KEY:
        await interaction.followup.send(
            embed=make_embed(
                "Challonge API Key Missing",
                "Create the API v1 key on Challonge, add `CHALLONGE_API_KEY=your_key_here` to `C:\\discord-bot\\.env`, then restart the bot.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "Create one first with `/tournament_create`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("challonge_url"):
        await interaction.followup.send(
            embed=make_embed(
                "Already Linked",
                "This tournament already has a Challonge link. Use `/challonge_unlink` first if you want to replace it.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    if len(tournament.get("players", [])) < 2:
        await interaction.followup.send(
            embed=make_embed("Not Enough Players", "Add at least 2 players before creating the Challonge bracket.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    try:
        challonge_url, participant_count = await create_and_link_challonge_v1_tournament(
            tournament,
            private=private,
            url_slug=url_slug,
        )
    except RuntimeError as error:
        tournament["challonge_error"] = str(error)
        await upsert_tournament_control_center(interaction.guild, tournament)
        save_tournaments(tournaments)
        await interaction.followup.send(
            embed=make_embed("Challonge Error", str(error)[:3900], ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("create Challonge tournament", tournaments=tournaments)
    tournament.pop("challonge_error", None)
    await upsert_tournament_control_center(interaction.guild, tournament)
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed(
            "Challonge Bracket Created",
            (
                f"Created Challonge bracket for **{tournament['name']}**.\n"
                f"Players synced: **{participant_count}**\n"
                f"{challonge_url}"
            ),
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="challonge_start", description="Start the linked Challonge tournament so scores can be reported.")
async def challonge_start(interaction: discord.Interaction):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    if not CHALLONGE_API_KEY:
        await interaction.followup.send(
            embed=make_embed(
                "Challonge API Key Missing",
                "Add `CHALLONGE_API_KEY=your_key_here` to `C:\\discord-bot\\.env`, then restart the bot.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "Create one first with `/tournament_create`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    tournament_identifier = get_challonge_identifier_from_tournament(tournament)

    if not tournament_identifier:
        await interaction.followup.send(
            embed=make_embed(
                "No Challonge Bracket",
                "Create one with `/challonge_create` first, or link one with `/challonge_link`.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    try:
        await start_challonge_v1_tournament(tournament_identifier)
    except RuntimeError as error:
        await interaction.followup.send(
            embed=make_embed("Challonge Start Failed", str(error)[:3900], ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("start Challonge tournament", tournaments=tournaments)
    tournament.setdefault("challonge", {})["started"] = True
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed(
            "Challonge Tournament Started",
            (
                "The Challonge bracket is now live.\n"
                "You can use `/score` and the bot will try to sync the result to Challonge."
            ),
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="score", description="Report a tournament scoreline and advance the bracket.")
async def score(
    interaction: discord.Interaction,
    player_one: discord.Member,
    player_one_goals: int,
    player_two: discord.Member,
    player_two_goals: int,
):
    if not await safe_defer(interaction):
        return

    if player_one.id == player_two.id:
        await interaction.followup.send(
            embed=make_embed("Duplicate Player", "Choose two different players.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if player_one_goals < 0 or player_two_goals < 0:
        await interaction.followup.send(
            embed=make_embed("Invalid Score", "Goals cannot be negative.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament or tournament.get("status") != "running":
        await interaction.followup.send(
            embed=make_embed("No Running Tournament", "There is no running tournament to report.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    match = find_open_tournament_match_by_players(tournament, player_one.id, player_two.id)

    if not match:
        await interaction.followup.send(
            embed=make_embed(
                "Match Not Found",
                f"I could not find an open tournament match between {player_one.mention} and {player_two.mention}.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    match_player_one = match.get("player_one")
    match_player_two = match.get("player_two")
    reported_scores = {
        str(player_one.id): player_one_goals,
        str(player_two.id): player_two_goals,
    }
    match_player_one_goals = reported_scores[str(match_player_one["id"])]
    match_player_two_goals = reported_scores[str(match_player_two["id"])]

    is_organiser = has_command_role_access(interaction)
    player_ids = {str(match_player_one["id"]), str(match_player_two["id"])}

    if not is_organiser and str(interaction.user.id) not in player_ids:
        await interaction.followup.send(
            embed=make_embed("Not Your Match", "Only the two match players or a tournament organiser can report this score.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if is_organiser:
        record_undo("organiser report tournament match", profiles=load_profiles(), tournaments=tournaments)
        result_state = apply_score_to_match(match, match_player_one_goals, match_player_two_goals)

        if result_state == "draw":
            match.pop("pending_score", None)
            await post_match_result(
                interaction.guild,
                tournament,
                match,
                title="Draw Reported",
                note="Replay needed before this match can advance.",
            )
            await upsert_round_control_center(interaction.guild, tournament)
        else:
            await finalize_tournament_match(interaction.guild, tournament, match)

        save_tournaments(tournaments)
        await interaction.followup.send(
            embed=make_embed(
                "Score Recorded",
                "The organiser score was recorded and the tournament was updated.",
                SUCCESS_COLOR,
            ),
            ephemeral=True,
        )
        return

    submitter_id = str(interaction.user.id)
    opponent_id = str(match_player_two["id"]) if submitter_id == str(match_player_one["id"]) else str(match_player_one["id"])
    record_undo("submit tournament score", tournaments=tournaments)
    match["pending_score"] = {
        "submitted_by": submitter_id,
        "player_one": match_player_one_goals,
        "player_two": match_player_two_goals,
    }

    save_tournaments(tournaments)

    score_text = f"{match_player_one_goals}-{match_player_two_goals}"
    embed = make_embed(
        "Score Confirmation Needed",
        (
            f"{interaction.user.mention} reported **{score_text}** for:\n"
            f"{tournament_player_label(match_player_one, interaction.guild)} vs {tournament_player_label(match_player_two, interaction.guild)}\n\n"
            f"<@{opponent_id}> must accept or reject this score."
        ),
        discord.Color.gold(),
    )
    view = ScoreApprovalView(tournament["id"], match["id"], opponent_id)

    await upsert_round_control_center(interaction.guild, tournament)
    await interaction.followup.send(
        content=f"<@{opponent_id}> score confirmation needed.",
        embed=embed,
        view=view,
        allowed_mentions=discord.AllowedMentions(users=True),
        ephemeral=False,
    )


@tree.command(name="dq", description="Disqualify a player from their current tournament match.")
async def dq(interaction: discord.Interaction, player: discord.Member):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament or tournament.get("status") != "running":
        await interaction.followup.send(
            embed=make_embed("No Running Tournament", "There is no running tournament to update.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    match = find_open_tournament_match_by_player(tournament, player.id)

    if not match:
        await interaction.followup.send(
            embed=make_embed(
                "Match Not Found",
                f"I could not find an open tournament match for {player.mention}.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    match_player_one = match.get("player_one")
    match_player_two = match.get("player_two")

    if not match_player_one or not match_player_two:
        await interaction.followup.send(
            embed=make_embed("Cannot DQ BYE", "This match does not have two real players.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    disqualified_id = str(player.id)

    if str(match_player_one["id"]) == disqualified_id:
        match["winner"] = match_player_two
        match["score"] = {"player_one": 0, "player_two": 1}
        opponent_label = tournament_player_label(match_player_two, interaction.guild)
    else:
        match["winner"] = match_player_one
        match["score"] = {"player_one": 1, "player_two": 0}
        opponent_label = tournament_player_label(match_player_one, interaction.guild)

    record_undo("disqualify tournament player", profiles=load_profiles(), tournaments=tournaments)
    match["state"] = "completed"
    match["dq"] = disqualified_id
    await finalize_tournament_match(interaction.guild, tournament, match)

    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed(
            "Player Disqualified",
            f"{player.mention} was disqualified. {opponent_label} advances with a **1-0** win.",
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="simulate_round", description="Test tool: randomly finish every open match in the current round.")
async def simulate_round(interaction: discord.Interaction):
    if not await safe_defer(interaction, ephemeral=True):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament or tournament.get("status") != "running":
        await interaction.followup.send(
            embed=make_embed("No Running Tournament", "There is no running tournament to simulate.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if not tournament.get("test_mode"):
        await interaction.followup.send(
            embed=make_embed(
                "Test Mode Required",
                "Turn on `/test_mode enabled:true` before simulating a round. This prevents profile rewards from being added by accident.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    open_matches = [
        match
        for match in get_current_round_matches(tournament)
        if match.get("state") in ("open", "draw") and match.get("player_one") and match.get("player_two")
    ]

    if not open_matches:
        await interaction.followup.send(
            embed=make_embed("Nothing To Simulate", "There are no open real-player matches in the current round.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("simulate tournament round", profiles=load_profiles(), tournaments=tournaments)
    completed_count = 0

    for match in open_matches:
        if random.choice([True, False]):
            player_one_goals = random.randint(1, 5)
            player_two_goals = random.randint(0, player_one_goals - 1)
        else:
            player_two_goals = random.randint(1, 5)
            player_one_goals = random.randint(0, player_two_goals - 1)

        apply_score_to_match(match, player_one_goals, player_two_goals)
        await finalize_tournament_match(interaction.guild, tournament, match, title="Simulated Result")
        completed_count += 1

    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed(
            "Round Simulated",
            f"Finished **{completed_count}** current-round matches with random results.\nUse `/next_round` to advance.",
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.command(name="next_round", description="Show round progress and start the next round when ready.")
async def next_round(interaction: discord.Interaction):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "No active tournament has been created yet.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("status") == "setup":
        await interaction.followup.send(
            embed=make_embed("Tournament Not Started", "Start the bracket first with `/tournament_start`.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    if tournament.get("status") == "completed":
        await upsert_round_control_center(interaction.guild, tournament)
        save_tournaments(tournaments)
        await interaction.followup.send(
            embed=make_embed("Tournament Completed", "The round control panel has been updated.", SUCCESS_COLOR),
            ephemeral=True,
        )
        return

    round_matches = get_current_round_matches(tournament)
    unfinished_matches = [match for match in round_matches if match.get("state") != "completed"]

    if unfinished_matches:
        await upsert_round_control_center(interaction.guild, tournament)
        save_tournaments(tournaments)
        await interaction.followup.send(
            embed=make_embed(
                "Round Still Open",
                "The round control panel has been updated. Finish all matches before starting the next round.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    previous_round = tournament.get("current_round", 1)
    record_undo("advance tournament round", tournaments=tournaments)
    advance_tournament_byes(tournament)
    await upsert_round_control_center(interaction.guild, tournament)
    dm_sent_count, dm_failed_count = await dm_next_round_opponents(interaction.guild, tournament)
    save_tournaments(tournaments)

    if tournament.get("status") == "completed":
        message = f"Round **{previous_round}** is complete. The tournament has a champion."
    else:
        message = f"Round **{previous_round}** is complete. Round **{tournament.get('current_round', previous_round)}** is now active."

        if dm_sent_count or dm_failed_count:
            message += f"\n\nOpponent DMs sent: **{dm_sent_count}**"

            if dm_failed_count:
                message += f"\nCould not DM: **{dm_failed_count}** players."

    await interaction.followup.send(
        embed=make_embed("Round Advanced", message, SUCCESS_COLOR),
        ephemeral=True,
    )


@tree.command(name="tournament_reset", description="Delete the active local tournament.")
async def tournament_reset(interaction: discord.Interaction):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()

    if not get_active_tournament(tournaments, interaction.guild):
        await interaction.followup.send(
            embed=make_embed("No Tournament", "There is no active tournament to reset.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("reset tournament", tournaments=tournaments)
    set_active_tournament(tournaments, interaction.guild, None)
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed("Tournament Reset", "The active tournament has been cleared.", SUCCESS_COLOR)
    )


@tree.command(name="tournament_end", description="End the active tournament so a new one can be created.")
async def tournament_end(interaction: discord.Interaction):
    if not await safe_defer(interaction):
        return

    if not await require_command_role(interaction):
        return

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if not tournament:
        await interaction.followup.send(
            embed=make_embed("No Tournament", "There is no active tournament to end.", ERROR_COLOR),
            ephemeral=True,
        )
        return

    record_undo("end tournament", tournaments=tournaments)
    tournament["status"] = "ended"
    tournament["ended_at"] = int(time.time())
    set_active_tournament(tournaments, interaction.guild, None)
    save_tournaments(tournaments)

    await interaction.followup.send(
        embed=make_embed(
            "Tournament Ended",
            (
                f"**{tournament['name']}** has been ended and removed as the active tournament.\n"
                "You can now create a fresh one with `/tournament_create`."
            ),
            SUCCESS_COLOR,
        )
    )


@tree.command(name="undo_last", description="Undo the last important saved data change.")
async def undo_last(interaction: discord.Interaction):
    if not await require_command_role(interaction):
        return

    undo_stack = load_undo_stack()

    if not undo_stack:
        await interaction.response.send_message(
            embed=make_embed(
                "Nothing To Undo",
                "There are no saved actions to undo.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    undo_item = undo_stack.pop()
    save_undo_stack(undo_stack)

    restored = []

    if undo_item.get("scores") is not None:
        save_scores(undo_item["scores"])
        restored.append("leaderboard")

    if undo_item.get("statcards") is not None:
        save_statcards(undo_item["statcards"])
        restored.append("stat cards")

    if undo_item.get("profiles") is not None:
        save_profiles(undo_item["profiles"])
        restored.append("profiles")

    if undo_item.get("round_robin") is not None:
        save_round_robin(undo_item["round_robin"])
        restored.append("CFI matchups")

    if undo_item.get("tournaments") is not None:
        save_tournaments(undo_item["tournaments"])
        restored.append("tournaments")

    restored_text = ", ".join(restored) if restored else "saved data"

    await interaction.response.send_message(
        embed=make_embed(
            "Undo Complete",
            f"Undid: **{undo_item['action']}**\nRestored: **{restored_text}**.",
            SUCCESS_COLOR,
        )
    )


SCORE_UNDO_ACTIONS = {
    "accept tournament score",
    "organiser report tournament match",
    "submit tournament score",
    "disqualify tournament player",
    "simulate tournament round",
}


@tree.command(name="undo_score", description="Undo the most recent tournament score change.")
async def undo_score(interaction: discord.Interaction):
    if not await require_command_role(interaction):
        return

    if not await safe_defer(interaction, ephemeral=True):
        return

    undo_stack = load_undo_stack()
    undo_index = None

    for index in range(len(undo_stack) - 1, -1, -1):
        if undo_stack[index].get("action") in SCORE_UNDO_ACTIONS:
            undo_index = index
            break

    if undo_index is None:
        await interaction.followup.send(
            embed=make_embed(
                "No Score To Undo",
                "I could not find a recent score action in the undo history.",
                ERROR_COLOR,
            ),
            ephemeral=True,
        )
        return

    current_tournaments = load_tournaments()
    current_tournament = get_active_tournament(current_tournaments, interaction.guild) if interaction.guild else None
    restored_tournament = None
    reopened_challonge_count = 0

    if undo_stack[undo_index].get("tournaments") is not None and interaction.guild:
        restored_tournament = get_active_tournament(undo_stack[undo_index]["tournaments"], interaction.guild)

    challonge_warnings = []

    if current_tournament and restored_tournament and current_tournament.get("challonge_url") and CHALLONGE_API_KEY:
        for match in find_matches_reopened_by_undo(current_tournament, restored_tournament):
            try:
                warning = await reopen_challonge_v1_match_for_local_match(current_tournament, match)

                if warning:
                    challonge_warnings.append(warning)
                else:
                    reopened_challonge_count += 1
            except RuntimeError as error:
                challonge_warnings.append(str(error))

    undo_item = undo_stack.pop(undo_index)
    save_undo_stack(undo_stack)
    restored = []

    if undo_item.get("profiles") is not None:
        save_profiles(undo_item["profiles"])
        restored.append("profiles")

    if undo_item.get("tournaments") is not None:
        save_tournaments(undo_item["tournaments"])
        restored.append("tournament bracket")

    tournaments = load_tournaments()
    tournament = get_active_tournament(tournaments, interaction.guild)

    if tournament and interaction.guild:
        await upsert_round_control_center(interaction.guild, tournament)

    restored_text = ", ".join(restored) if restored else "score state"
    challonge_text = ""

    if challonge_warnings:
        challonge_text = "\n\nChallonge warning: " + "; ".join(challonge_warnings[:3])
    elif reopened_challonge_count:
        challonge_text = "\n\nChallonge match reopened too."

    await interaction.followup.send(
        embed=make_embed(
            "Score Undo Complete",
            f"Undid: **{undo_item['action']}**\nRestored: **{restored_text}**.{challonge_text}",
            SUCCESS_COLOR,
        ),
        ephemeral=True,
    )


@tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    print(f"Command error: {error}")
    traceback.print_exception(type(error), error, error.__traceback__)

    try:
        if interaction.response.is_done():
            await interaction.followup.send(
                "Something went wrong while running that command. Check the bot console.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "Something went wrong while running that command. Check the bot console.",
                ephemeral=True,
            )
    except discord.HTTPException as send_error:
        if send_error.code != 40060:
            print(f"Could not send command error response: {send_error}")


try:
    client.run(TOKEN)
except discord.LoginFailure:
    raise SystemExit(
        "Discord rejected the token in C:\\discord-bot\\.env.\n"
        "Reset the token in the Discord Developer Portal, paste the new one, and try again."
    )

