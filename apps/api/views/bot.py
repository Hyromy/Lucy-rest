from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .. import models
from .. import serializers

class GuildView(APIView):
    @staticmethod
    def _requires_id(func):
        def wrapper(*args, **kwargs):
            if 'id' not in kwargs or kwargs['id'] is None:
                return Response(
                    {"error": "ID is required for this operation"},
                    status = status.HTTP_400_BAD_REQUEST
                )
            return func(*args, **kwargs)
        return wrapper

    @_requires_id
    def get(self, request, id = None):
        try:
            guild = models.Guild.objects.get(id = id)
            serializer = serializers.GuildSerializer(guild)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        except models.Guild.DoesNotExist:
            return Response({"error": "Guild not found"}, status = status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        serializer = serializers.GuildSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"ok": True, "msg": "Guild created successfully"},
                status = status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    @_requires_id
    def patch(self, request, id = None):
        if request.data == {}:
            return Response(
                {"ok": True, "msg": "No changes made as no data was provided"},
                status = status.HTTP_200_OK
            )
        try:
            guild = models.Guild.objects.get(id = id)
            serializer = serializers.GuildSerializer(guild, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"ok": True, "msg": "Guild updated successfully"},
                    status = status.HTTP_200_OK
                )
            
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        except models.Guild.DoesNotExist:
            return Response({"error": "Guild not found"}, status = status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @_requires_id
    def delete(self, request, id = None):
        try:
            guild = models.Guild.objects.get(id = id)
            models.DeletedGuild(
                guild_id = guild.id,
                name = guild.name
            ).save()
            guild.delete()
            
            return Response(
                {"ok": True, "msg": "Guild deleted successfully"},
                status = status.HTTP_200_OK
            )
        
        except models.Guild.DoesNotExist:
            return Response({"error": "Guild not found"}, status = status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
