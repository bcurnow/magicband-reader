from magicbandreader.event import Event, EventType


def test_Event__init__():
    e = Event('rfid_id', {'context': True}, EventType.NONE)

    assert e.id == 'rfid_id'
    assert e.ctx == {'context': True}
    assert e.type == EventType.NONE
    assert e.__repr__() == "Event('rfid_id', {'context': True}, EventType.NONE)"
    assert e.__str__() == e.__repr__()
