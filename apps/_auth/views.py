from aiohttp import ClientSession
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
from os import getenv

@require_GET
async def discord(request):
    redirect_uri = ("http://localhost:5173" if settings.DEBUG else "https://lucy.hyromy.xyz") + "/"

    code = request.GET.get("code")

    if not code:
        return JsonResponse(
            {
                "error": "Missing code",
                "message": "The 'code' query parameter is required."
            },
            status = 400
        )

    async with ClientSession() as session:
        async with session.post(
            "https://discord.com/api/oauth2/token",
            data = {
                "client_id": getenv("DISCORD_CLIENT_ID"),
                "client_secret": getenv("DISCORD_CLIENT_SECRET"),
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri + getenv("FRONTEND_URL_ENDPOINT", "auth/callback"), 
            },
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        ) as resp:
            if resp.status != 200:
                return JsonResponse(
                    {
                        "error": "Failed to retrieve token",
                        "message": "Could not retrieve access token from Discord.",
                        "response": await resp.json()
                    },
                    status = resp.status
                )
            
            return JsonResponse(await resp.json())
