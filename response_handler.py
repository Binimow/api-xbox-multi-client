from typing import Dict
import json
import os
from xbox.webapi.api.provider.profile.models import ProfileUser

from clients_manager import ClientsManager
from models import ManagerMessage

async def createResponseHandler(filename_name_id: str, clients_manager: ClientsManager):
    responseHandler = ResponseHandler(filename_name_id, clients_manager)
    await responseHandler.load()
    return responseHandler

class ResponseHandler():
    '''Handle the responses given to the client. Make the client available for the ClientManager.'''
    def __init__(self, filename_name_id: str, clients_manager: ClientsManager):
        self.filename_name_id = filename_name_id
        self.clients_manager = clients_manager
        self.name_id: list[Dict[str, str]] = []

    async def load(self):
        if os.path.exists(self.filename_name_id):
            with open(self.filename_name_id, 'r') as in_file:
                self.name_id = json.loads(in_file.read())
        else:
            print('WARNING: The file for the name-id file provided in the ResponseHandler does not exist')
    
    def save(self):
        print("saved response handler")
        if os.path.exists(self.filename_name_id):
            with open(self.filename_name_id, 'w') as out_file:
                print(self.name_id)
                out_file.write(json.dumps(self.name_id))
        else:
            print('WARNING: The file for the name-id file provided in the ResponseHandler does not exist')
        print("succesfully saved")

    async def receive_gamertag(self, gamertag: str, response: ProfileUser, clientid: str):
        '''Receive the id associated with a gamertag from the client'''
        self.name_id.append({
            'uid': response.id,
            'gamertag': gamertag
        })
        print('received gamertag')
        await self.clients_manager.notify_manager(clientid, ManagerMessage.WAITING)
