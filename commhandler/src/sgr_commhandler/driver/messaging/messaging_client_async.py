"""
Provides the messaging client implementation.
"""

import logging
from abc import ABC
from typing import Any, Callable, NoReturn, Optional
from gmqtt import Client as MQTTClient
import asyncio


logger = logging.getLogger(__name__)


class SGrMessagingClient(ABC):
    """
    Defines an abstract base class for messaging clients.
    """

    async def connect(self):
        ...

    async def disconnect(self):
        ...

    def is_connected(self) -> bool:
        ...

    async def publish_async(self, topic: str, payload: Any):
        ...

    async def subscribe_async(self, topic: str):
        ...

    async def unsubscribe_async(self, topic: str):
        ...

    def set_message_handler(self, handler: Callable[[str, Any], NoReturn]):
        ...


class SGrMqttClient(SGrMessagingClient):
    """
    Implements an MQTT messaging client.
    """

    def __init__(self, host: str, port: int, client_id: str, tls: bool = False, credentials: Optional[tuple[str, str]] = None):
        self._host = host
        self._port = port
        self._tls = tls
        self._on_message_handler: Optional[Callable[[str, Any], NoReturn]] = None

        self._client = MQTTClient(client_id, clean_session=True)
        self._client.on_connect = self._on_client_connect
        self._client.on_disconnect = self._on_client_disconnect
        self._client.on_subscribe = self._on_client_subscribe
        self._client.on_unsubscribe = self._on_client_unsubscribe
        self._client.on_message = self._on_client_message
        if credentials is not None:
            self._client.set_auth_credentials(credentials[0], credentials[1])

    async def connect(self):
        await self._client.connect(self._host, self._port, ssl=self._tls, keepalive=60)

    async def disconnect(self):
        await self._client.disconnect()

    def is_connected(self) -> bool:
        return self._client.is_connected

    async def publish_async(self, topic: str, payload: Any):
        # TODO support QoS levels
        qos = 0
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._client.publish, topic, payload, qos)
        logger.debug(f"{self._client._client_id} sent message on '{topic}': payload='{type(payload)}' qos={qos}")

    async def subscribe_async(self, topic: str):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._client.subscribe, topic)

    async def unsubscribe_async(self, topic: str):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._client.unsubscribe, topic)

    def set_message_handler(self, handler: Callable[[str, Any], NoReturn]):
        self._on_message_handler = handler

    def _on_client_connect(self, client, flags, rc, properties):
        logger.debug(f'{client._client_id} connected')

    def _on_client_disconnect(self, client, packet):
        # packet is just a byte array
        logger.debug(f'{client._client_id} disconnected')

    def _on_client_subscribe(self, client, mid, qos, properties):
        # mid is an ID
        logger.debug(f'{client._client_id} subscribed to {mid}')

    def _on_client_unsubscribe(self, client, mid, qos):
        # mid is an ID
        logger.debug(f'{client._client_id} unsubscribed from {mid}')

    def _on_client_message(self, client, topic, payload, qos, properties):
        # payload is a byte array
        logger.debug(f"{client._client_id} received message on '{topic}': payload='{type(payload)}' qos={qos}")
        if self._on_message_handler is not None:
            self._on_message_handler(topic, payload)
