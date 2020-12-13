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
        return self.__repr__()

    def __repr__(self):
        return f"Event('{self.id}', {self.ctx}, {self.type})"
