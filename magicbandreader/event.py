from collections import namedtuple
from enum import Enum, auto


class EventType(Enum):
    NONE = auto()
    AUTHORIZED = auto()
    UNAUTHORIZED = auto()


class Event():
    def __init__(self, rfid_id, ctx, type=None):
        self.id = rfid_id
        self.ctx = ctx
        self.type = type

    def __str__(self):
        return f'Event(id: {self.id}, type: {self.type}, ctx: {self.ctx})'

    def __repr__(self):
        return self._str__()
