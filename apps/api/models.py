from django.db import models

class Guild(models.Model):
    id = models.BigIntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    icon = models.CharField(max_length = 32, null = True, blank = True)
    banner = models.CharField(max_length = 32, null = True, blank = True)

    lang = models.CharField(
        max_length = 2,
        default = 'en',
        choices = [
            ('en', 'English'),
            ('es', 'Español'),
        ]
    )
    joined_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.name} ({self.id})"

class DeletedGuild(models.Model):
    id = models.BigAutoField(primary_key = True)
    guild_id = models.BigIntegerField()
    name = models.CharField(max_length = 100)
    deleted_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
