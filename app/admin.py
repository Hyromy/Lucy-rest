from django.contrib import admin

from app import models

admin.site.register(models.Guild)
admin.site.register(models.DeletedGuild)
