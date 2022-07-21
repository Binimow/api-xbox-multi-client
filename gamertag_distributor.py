import asyncio
import json
import pickle
import sys
from typing import Dict
from typing import Type
import os.path

async def createGamertagDistributor(filename_self: str, filename_gamertags: str):
    gt_distributor = GamertagDistributor(filename_self, filename_gamertags)
    await gt_distributor.load()
    return gt_distributor

class GamertagDistributor():
    def __init__(self, filename_self: str, filename_gamertags: str):
        self.index = 0
        self.gamertags: list[str] = []
        self.filename_self = filename_self
        self.filename_gamertags = filename_gamertags
        if not os.path.exists(filename_gamertags):
            sys.exit("The file containing the gamertags wasnt found")            

    def next(self) -> str:
        gamertag = self.gamertags[self.index]
        self.index += 1
        return gamertag

    async def load(self):
        await asyncio.gather(
            self.load_self(),
            self.load_gamertags()
        )

    async def load_self(self):
        if os.path.exists(self.filename_self):
            with open(self.filename_self, 'rb') as in_file:
                temp_dict = pickle.load(in_file)
            self.__dict__['index'] = temp_dict['index']

    async def load_gamertags(self):
        with open(self.filename_gamertags, 'r') as in_file:
            file_content = in_file.read()
            self.gamertags = list(map(
                str.strip,
                file_content.split(',')
            ))

    async def save(self):
        with open(self.filename_self, 'wb') as out_file:
            pickle.dump(self.__dict__, out_file)