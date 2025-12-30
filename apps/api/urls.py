from django.urls import path
from . import views

urlpatterns = [
    path("", views.HealthCheckView.as_view()),
    path("guild/<int:id>/", views.GuildView.as_view()),
    path("guild/", views.GuildView.as_view()),
]
