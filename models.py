from dataclasses import dataclass
from enum import Enum

class ClientMessage(Enum):
    '''Message sent to the client'''
    START = "Start"
    REQUEST_GAMERTAG = "RequestGamertag"
    PINGREQ = "PingReq"

class ManagerMessage(Enum):
    '''Message sent to the manager'''
    AVAILABLE = "Available"
    WAITING = "Waiting"
    BUSY = "Busy"

class APICategory(Enum):
    '''The API category'''
    STATS = "stats"
    PROFILE = "profile"
    MPSD = "mpsd"
    SEARCH = "search_handle"
    PRESENCE = "presence"
    SOCIAL = "social"
    LEADERBOARD = "leaderboards"
    ACHIEVEMENTS = "achievements" 
    SMART = "smart"
    USER = "user"
    PRIVACY = "privacy"
    CLUBS = "club"
    COLLECTIONS = "collections"
    INVENTORY = "inventory"

@dataclass
class ClientRequestHistory:
    request_history: dict[APICategory, list[float]] #float represent time in second  