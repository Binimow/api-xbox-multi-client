import json
import pickle
import sys
import asyncio
import time
from aiohttp import ClientResponseError, ClientSession
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.common.exceptions import AuthenticationException
import numpy as np
import collections.abc
from client import XboxLiveClientCustom
from clients_manager import ClientsManager
from gamertag_distributor import GamertagDistributor, createGamertagDistributor
from models import ClientMessage, ManagerMessage
from response_handler import ResponseHandler, createResponseHandler

collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
collections.Generator = collections.abc.Generator
from linq import Flow
from xbox import *
client_id = '42c09027-c9fa-4ee9-b92e-d0b1cd8abf5b'
client_secret = '2dr8Q~Nq39txP.WYyOIWW8bgZ5JUBmAE5kkbqcwF'
"""
For doing authentication, see xbox/webapi/scripts/authenticate.py
"""

async def async_main():
    # replace with path in auth scrip or just paste file with tokens here
    tokens_file = "./data/tokens.json"
    async with ClientSession() as session:
        auth_mgr = AuthenticationManager(
            session, client_id, client_secret, ""
        )

        try:
            with open(tokens_file, mode="r") as f:
                tokens = f.read()
            auth_mgr.oauth = OAuth2TokenResponse.parse_raw(tokens)
        except FileNotFoundError:
            print(
                f'File {tokens_file} isn`t found or it doesn`t contain tokens!')
            exit(-1)
        try:
            await auth_mgr.refresh_tokens()
        except ClientResponseError:
            print("Could not refresh tokens")
            sys.exit(-1)
        with open(tokens_file, mode="w") as f:
              f.write(auth_mgr.oauth.json())
        print(f'Refreshed tokens in {tokens_file}!')

        gt_distributor = await createGamertagDistributor('./data/gamertag_distributor.bin', './data/name-list.txt')
        clients_manager = ClientsManager(gt_distributor)
        response_handler = await createResponseHandler('./data/name-id.json', clients_manager)
        xbl_client1 = XboxLiveClientCustom(auth_mgr, response_handler)
        clients_manager.add_client(xbl_client1)
        await clients_manager.broadcast_client(ClientMessage.START)
        await gt_distributor.save()
        await response_handler.save()
        await asyncio.gather(*[client.check_availability() for client in clients_manager.clients.values()]) #will never stop


asyncio.get_event_loop_policy().get_event_loop().run_until_complete(async_main())
