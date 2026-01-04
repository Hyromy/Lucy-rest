from aiohttp import ClientSession, ClientTimeout, ClientError
from os import getenv

from django.conf import settings

DISCORD_API_BASE = "https://discord.com/api/v10"

async def get_discord_user_guilds(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        async with ClientSession() as session:
            async with session.get(
                f"{DISCORD_API_BASE}/users/@me/guilds",
                headers = headers,
                timeout = ClientTimeout(total = 10)
            ) as response:
                
                if response.status == 200:
                    guilds = await response.json()
                    return {"ok": True, "guilds": guilds}
                
                elif response.status == 401:
                    return {"ok": False, "error": "Invalid or expired token"}
                
                else:
                    return {"ok": False, "error": f"Discord API error: {response.status}"}
                    
    except ClientError as e:
        return {"ok": False, "error": f"Request failed: {str(e)}"}
    
    except Exception as e:
        return {"ok": False, "error": f"Unexpected error: {str(e)}"}

async def get_discord_guild_details(guild_id):
    token = getenv(("DEV" if settings.DEBUG else "PRO") + "_DISCORD_BOT_TOKEN")
    if not token:
        return {"ok": False, "error": "Bot token not configured"}
    
    try:
        async with ClientSession() as session:
            async with session.get(
                f"{DISCORD_API_BASE}/guilds/{guild_id}",
                headers = {
                    'Authorization': f'Bot {token}'
                },
                timeout = ClientTimeout(total = 10)
            ) as response:
                if response.status == 200:
                    guild = await response.json()
                    return {"ok": True, "guild": guild}
                
                elif response.status == 404:
                    return {"ok": False, "error": "Guild not found or bot not in guild"}
                
                elif response.status == 401:
                    return {"ok": False, "error": "Invalid bot token"}
                
                else:
                    return {"ok": False, "error": f"Discord API error: {response.status}"}
                    
    except ClientError as e:
        return {"ok": False, "error": f"Request failed: {str(e)}"}
    
    except Exception as e:
        return {"ok": False, "error": f"Unexpected error: {str(e)}"}

def filter_admin_guilds(guilds):
    ADMINISTRATOR = 0x8
    MANAGE_GUILD = 0x20
    
    admin_guilds = []
    for guild in guilds:
        permissions = int(guild.get('permissions', 0))
        if (permissions & ADMINISTRATOR) or (permissions & MANAGE_GUILD):
            admin_guilds.append(guild)
    
    return admin_guilds

def make_simple_guild_dict(guild_data):
    return {
        "id": guild_data.get("id"),
        "name": guild_data.get("name"),
        "icon": guild_data.get("icon"),
        "banner": guild_data.get("banner"),
        "owner": guild_data.get("owner")
    }
