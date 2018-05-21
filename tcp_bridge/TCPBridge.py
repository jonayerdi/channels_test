#!/usr/bin/python

import threading
import socket
import queue
import logging

class TCPBridgeConnection(threading.Thread):
	def __init__(self, server, sock, address):
		super().__init__()
		self.logger = server.logger
		self.server = server
		self.sock = sock
		self.address = address

	def run(self):
		self.logger.info('Connection accepted from {}'.format(self.address))
		try:
			while True:
				data = self.sock.recv(4096)
				if not data:
					raise ConnectionError()
				self.logger.info('{} bytes received from {}'.format(len(data), self.address))
				with self.server.consumersLock:
					for consumer in self.server.consumers:
						consumer.send_json({"text": data})
		except ConnectionError:
			pass
		self.sock.close()
		with self.server.connectionsLock:
			self.server.connections.remove(self)
		self.logger.info('Disconnected from {}'.format(self.address))

class TCPBridge(threading.Thread):
	def __init__(self, ip='127.0.0.1', port=6969, logger=logging.getLogger()):
		super().__init__()
		self.logger = logger
		self.ip = ip
		self.port = port
		self.sock = None
		self.connections = []
		self.consumers = []
		self.connectionsLock = threading.Lock()
		self.consumersLock = threading.Lock()

	def run(self):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((self.ip, self.port))
			self.sock.listen()
		except Exception as e:
			self.logger.error('Exception binding socket: {}'.format(e))
			return

		self.logger.info('Accepting connections to {}:{}'.format(self.ip, self.port))
		try:
			while True:
				conn, addr = self.sock.accept()
				connection = TCPBridgeConnection(self, conn, addr)
				with self.connectionsLock:
					self.connections.append(connection)
				connection.start()
		except Exception as e:
			self.logger.error('Exception accepting connections: {}'.format(e))
		finally:
			self.sock.close()
