from django.urls import path
from . import views

urlpatterns = [
    path("discord/", views.discord)
]
