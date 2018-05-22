from channels.generic.websocket import WebsocketConsumer
from .TCPBridge import TCPBridge
import logging

log = logging.getLogger('TCPBridge')
tcpBridge = TCPBridge(ip='127.0.0.1', port=6969, logger=log)
tcpBridge.start()

class WSConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        with tcpBridge.consumersLock:
            tcpBridge.consumers.append(self)
        log.info('WebSocket connect')

    def receive(self, text_data):
        log.info('WebSocket receive: {}'.format(text_data))

    def disconnect(self, code):
        with tcpBridge.consumersLock:
            tcpBridge.consumers.remove(self)
        log.info('WebSocket disconnect: {}'.format(code))
