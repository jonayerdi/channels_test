from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import tcp_bridge.routing

from tcp_bridge.consumers import WSConsumer

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            tcp_bridge.routing.websocket_urlpatterns
        )
    ),
})
