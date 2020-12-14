from magicbandreader.authorize import RfidSecuritySvcAuthorizer
from magicbandreader.event import EventType
from magicbandreader.handlers import AbstractHandler


class EventTypeHandler(AbstractHandler):
    """ Sets the EventType by using an authorizer. This handler should come before any handler that relies on the event type."""
    def __init__(self, ctx, authorizer):
        super().__init__(priority=10)
        self.ctx = ctx
        # Populate the context with the authorizer instance
        self.ctx.authorizer = authorizer

    def handle_event(self, event):
        """ Override the handle_event method from the super class as it won't be authorized yet since we're doing that."""

        if event.id:
            if self.ctx.authorizer.authorized(event.id):
                event.type = EventType.AUTHORIZED
            else:
                event.type = EventType.UNAUTHORIZED
        else:
            event.type = EventType.NONE


def register(ctx):
    return EventTypeHandler(ctx, RfidSecuritySvcAuthorizer(ctx))
