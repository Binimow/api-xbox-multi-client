from enum import Enum

class ClientMessage(Enum):
    '''Message sent to the client'''
    START = "Start"
    REQUEST_GAMERTAG = "RequestGamertag"
    PINGREQ = "PingReq"

class ManagerMessage(Enum):
    '''Message sent to the manager'''
    AVAILABLE = "Available"
    BUSY = "Busy"