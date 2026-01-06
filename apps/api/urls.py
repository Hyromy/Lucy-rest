from django.urls import path

from .views import (
    health,
    bot,
    dashboard
)

urlpatterns = [
    path("", health.HealthCheckView.as_view()),
]

urlpatterns += [
    path(f"dashboard/{d['route']}", d['view']) for d in [
        {"route": "guild/", "view": dashboard.GuildView.as_view()},
        {"route": "guild/<int:id>/", "view": dashboard.GuildView.as_view()},
    ]
]

urlpatterns += [
    path(f"bot/{b['route']}", b['view']) for b in [
        {"route": "guild/", "view": bot.GuildView.as_view()},
        {"route": "guild/<int:id>", "view": bot.GuildView.as_view()},
    ]
]
