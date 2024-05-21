from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from hestia_api.consumers import CommandConsumer
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    path('ws/command/', CommandConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': URLRouter(websocket_urlpatterns)
})