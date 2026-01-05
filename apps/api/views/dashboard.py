from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import sync_to_async

from decorators.validations import require_token

from ..utils.discord import (
    get_discord_user_guilds,
    filter_admin_guilds,
    make_simple_guild_dict,
    get_discord_guild_details,
)
from ..models import Guild

class GuildView(APIView):
    @require_token
    async def get(self, request, id = None):
        token = request.validated_token
        if not id:
            try:
                guilds = filter_admin_guilds((await get_discord_user_guilds(token))["guilds"])
            except Exception as e:
                return Response(
                    {
                        "ok": False,
                        "error": str(e)
                    },
                    status = status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            discord_guild_ids = [int(guild["id"]) for guild in guilds]
            
            registered_ids = await sync_to_async(set)(
                Guild.objects.filter(id__in = discord_guild_ids).values_list('id', flat = True)
            )
            
            registered_guilds = []
            ready_to_install_guilds = []
            
            for guild in guilds:
                guild_id = int(guild["id"])
                if guild_id in registered_ids:
                    registered_guilds.append(make_simple_guild_dict(guild))
                else:
                    ready_to_install_guilds.append(make_simple_guild_dict(guild))

            return Response(
                {
                    "ok": True,
                    "registered_guilds": registered_guilds,
                    "ready_to_install_guilds": ready_to_install_guilds
                    
                },
                status = status.HTTP_200_OK
            )
        
        guild_details_response = await get_discord_guild_details(id)
        if not guild_details_response["ok"]:
            return Response(
                guild_details_response,
                status = status.HTTP_400_BAD_REQUEST
            )

        guild_data = guild_details_response["guild"]
        try:
            db_guild = await sync_to_async(Guild.objects.get)(id = id)
            guild_data["lang"] = db_guild.lang
            guild_data["joined_at"] = db_guild.joined_at.isoformat()
        except Guild.DoesNotExist:
            pass
        
        return Response(
            {
                "ok": True,
                "guild": guild_data
            },
            status = status.HTTP_200_OK
        )
