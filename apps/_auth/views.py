from aiohttp import ClientSession
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from json import loads, JSONDecodeError
from os import getenv

@csrf_exempt
@require_POST
async def discord(request):
    try:
        data = loads(request.body)
    except JSONDecodeError:
        return JsonResponse(
            {
                "error": "Invalid JSON",
                "message": "The request body must be valid JSON."
            },
            status = 400
        )

    code = data.get("code")
    if not code:
        return JsonResponse(
            {
                "error": "Missing code",
                "message": "The 'code' parameter is required in the request body."
            },
            status = 400
        )

    origin = (request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER', '')).rstrip('/')
    endpoint = getenv('FRONTEND_URL_ENDPOINT', 'auth/callback').lstrip('/')
    if origin:
        redirect_uri = f"{origin}/{endpoint}"
    else:
        localhost = "http://localhost:5173"
        redirect_uri = (
            (localhost if settings.DEBUG else getenv("FRONTEND_URL", localhost)) + "/" + endpoint
        )

    async with ClientSession() as session:
        async with session.post(
            "https://discord.com/api/oauth2/token",
            data = {
                "client_id": getenv("DISCORD_CLIENT_ID"),
                "client_secret": getenv("DISCORD_CLIENT_SECRET"),
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri
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
