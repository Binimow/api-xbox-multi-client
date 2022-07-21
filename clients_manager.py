from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Dict
from gamertag_distributor import GamertagDistributor
if TYPE_CHECKING:
    from client import XboxLiveClientCustom
from models import ClientMessage, ManagerMessage

class ClientsManager:
    def __init__(self, gt_distributor: GamertagDistributor):
        self.clients: Dict[str, XboxLiveClientCustom] = {}
        self.gt_distributor = gt_distributor
        self.loop = asyncio.get_running_loop()
        self.set_client_manager()

    def set_client_manager(self): 
        '''Set client manager for clients'''
        for client in list(self.clients.values()):
            client.set_manager(self)

    def add_client(self, client: XboxLiveClientCustom):
        '''Add the client to the clients list and set its manager as this client manager'''
        self.clients[client.clientid] = client
        client.set_manager(self)

    async def notify_manager(self, clientid: str, message=ManagerMessage.AVAILABLE): 
        '''This manager is being notified by a client'''
        client = self.clients.get(clientid)
        match message:
            case ManagerMessage.AVAILABLE:
                await self.clients[clientid].notify_client(message=ClientMessage.REQUEST_GAMERTAG, gamertag=self.gt_distributor.next())

    async def broadcast_client(self, message: ClientMessage, args=None):
        '''Send a message to all clients'''
        for client in self.clients.values():
            await client.notify_client(message)