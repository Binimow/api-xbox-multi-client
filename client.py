from __future__ import annotations
import typing

from response_handler import ResponseHandler
if typing.TYPE_CHECKING:
    from clients_manager import ClientsManager
from xbox.webapi.api.client import XboxLiveClient
from models import ClientMessage, ManagerMessage

class XboxLiveClientCustom(XboxLiveClient):
    def __init__(self, auth_mgr, response_handler: ResponseHandler):
        self.clientid = str(id(self))
        self.response_handler = response_handler
        super().__init__(auth_mgr=auth_mgr)
    
    def set_manager(self, manager: ClientsManager):
        '''Set the manager parent for the client'''
        self.manager = manager

    async def notify_manager(self, message: ManagerMessage): 
        '''Send a notification to the manager''' 
        await self.manager.notify_manager(self.clientid, message)
    
    async def notify_client(self, message: ClientMessage, **kwargs):
        '''Receive a notification from the manager'''
        match message:
            case ClientMessage.START:
                await self.notify_manager(message=ManagerMessage.AVAILABLE)
            case ClientMessage.PINGREQ:
                print(f"Client alive: {self.clientid}")
            case ClientMessage.REQUEST_GAMERTAG:
                gamertag: str = kwargs['gamertag']
                if type(gamertag) != str:
                    print(f'Argument type excepted: str, argument received: {type(gamertag)}')
                await self.request_gamertag(gamertag)
    
    async def request_gamertag(self, gamertag: str):
        '''Send a request to the XBOX api for the ID associated with a Gamertag'''
        result = await self.profile.get_profile_by_gamertag(gamertag)
        self.response_handler.receive_gamertag(gamertag, result.profile_users[0])
