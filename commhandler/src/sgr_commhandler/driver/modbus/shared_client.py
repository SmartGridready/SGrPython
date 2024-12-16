import asyncio
import logging
from threading import Lock

from sgr_specification.v0.product.modbus_types import BitOrder

from sgr_commhandler.driver.modbus.modbus_client_async import (
    SGrModbusClient,
    SGrModbusRTUClient,
)

logger = logging.getLogger(__name__)


class ModbusClientWrapper:
    def __init__(
        self, identifier: str, client: SGrModbusClient, shared: bool = False
    ):
        self.identifier = identifier
        self.client = client
        self.shared = shared
        self.registered_devices = set()
        self.connected_devices = set()

    async def connect(self, device_id: str):
        if self.shared:
            if device_id not in self.registered_devices:
                return
            if device_id not in self.connected_devices:
                self.connected_devices.add(device_id)
                logger.debug(
                    f'device {device_id} connected to shared Modbus client {self.identifier}'
                )
                await self.client.connect()
        else:
            await self.client.connect()

    async def disconnect(self, device_id: str):
        if self.shared:
            if device_id not in self.registered_devices:
                return
            if device_id in self.connected_devices:
                self.connected_devices.remove(device_id)
                logger.debug(
                    f'device {device_id} disconnected from shared Modbus client {self.identifier}'
                )
                if len(self.connected_devices) == 0:
                    logger.debug(
                        f'last device disconnected from shared Modbus client {self.identifier}'
                    )
                    await self.client.disconnect()
        else:
            await self.client.disconnect()

    def is_connected(self, device_id: str) -> bool:
        if self.shared:
            return (device_id in self.registered_devices) and (
                device_id is self.connected_devices
            )
        else:
            return self.client.is_connected()


# singleton objects
_global_shared_lock = Lock()
_global_shared_rtu_clients: dict[str, ModbusClientWrapper] = dict()


def register_shared_client(
    serial_port: str, parity: str, baudrate: int, device_id: str
) -> ModbusClientWrapper:
    global _global_shared_lock
    global _global_shared_rtu_clients
    with _global_shared_lock:
        client_wrapper = _global_shared_rtu_clients.get(serial_port)
        if client_wrapper is None:
            modbus_client = SGrModbusRTUClient(
                serial_port,
                parity,
                baudrate,
                BitOrder.BIG_ENDIAN,  # TODO bit order was missing, i just added want.
            )
            client_wrapper = ModbusClientWrapper(
                serial_port, modbus_client, shared=True
            )
            _global_shared_rtu_clients[serial_port] = client_wrapper
        client_wrapper.registered_devices.add(device_id)
        logger.debug(
            f'device {device_id} registered at shared Modbus client {client_wrapper.identifier}'
        )

        return client_wrapper


def unregister_shared_client(serial_port: str, device_id: str) -> None:
    global _global_shared_lock
    global _global_shared_rtu_clients
    with _global_shared_lock:
        client_wrapper = _global_shared_rtu_clients.get(serial_port)
        if client_wrapper is not None:
            client_wrapper.connected_devices.remove(device_id)
            client_wrapper.registered_devices.remove(device_id)
            if len(client_wrapper.registered_devices) == 0:
                try:
                    asyncio.get_event_loop().run_until_complete(
                        client_wrapper.client.disconnect()
                    )
                except Exception:
                    logger.warning(
                        f'could not disconnect shared transport {client_wrapper.identifier}'
                    )
                _global_shared_rtu_clients.pop(serial_port)
            logger.debug(
                f'device {device_id} unregistered from shared Modbus client {client_wrapper.identifier}'
            )
