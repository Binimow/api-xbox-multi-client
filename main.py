import json
import pickle
import sys
import asyncio
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
    gt_distributor = await createGamertagDistributor('./data/gamertag_distributor.bin', './data/name-list.txt')
    response_handler = await createResponseHandler('./data/name-id.json')
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
        
        xbl_client1 = XboxLiveClientCustom(auth_mgr, response_handler)
        clients_manager = ClientsManager(gt_distributor)
        clients_manager.add_client(xbl_client1)
        await clients_manager.broadcast_client(ClientMessage.START)
        await gt_distributor.save()
        await response_handler.save()
        # with open('./data/name-list.txt', 'r') as in_name_file:
        #     list_name = in_name_file.read().split(',')
        # for i in range(progress.index, progress.index + 10):
        #     progress.next(
        #         {
        #             "uid": (await xbl_client1.profile.get_profile_by_gamertag(list_name[i])).profile_users[0].id,
        #             "gamertag": list_name[i]
        #         }
        #     )

        # # Get presence status (by list of XUID)
        # presence = await xbl_client.presence.get_presence_batch(["2533274794093122", "2533274807551369"])
        # print('Statuses of some random players by XUID:')
        # print(presence)
        # print()

        # profiles = await xbl_client.profile.get_profiles(['2535459914186321', '2702159776423551'])
        # print(
        #     [
        #         profile.settings[
        #             [i for i in range(len(profile.settings)) if profile.settings[i].id == 'Gamertag'][0] #the list will always be a single element as we search by id
        #         ].value 
        #         for profile 
        #         in profiles.profile_users
        #     ]
        # )
            # What as been done yet: For now we have been able to use and authentify to the xbox.api and make calls on it.
            # We have two objectives now. 
            # First, we want to be able to get the id associated with a gamertag. If there is no id associated
            # with it, we know the gamertag is free.
            # Second, now that we have the ids, we can also call other services that need the ID to be working.
            # This way, the throttle limit of a client on a specific service xbox service could be surpassed as multiple 
            # services with there own throttle limit could be used by each client to resolve the final objective. 


asyncio.get_event_loop_policy().get_event_loop().run_until_complete(async_main())
