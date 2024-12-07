from django.urls import path
from .consumer import ChatConsumer

# the empty string routes to ChatConsumer, which manages the chat functionality.
websocket_urlpatterns = [
    path("messenger/<int:id>/", ChatConsumer.as_asgi()),
]