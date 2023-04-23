import unittest
import json
from RemoteHotKey.OneTimeEvent import OneTimeEvent


class OneTimeEventTest(unittest.TestCase):

    def test_init(self):
        event = OneTimeEvent()
        self.assertIsNone(event.getName())
        self.assertIsNone(event.getTimeStamp())

        json_str = '{"name": "Event1", "timeStamp": 1648226400.0}'
        event_from_json = OneTimeEvent(json_str)
        self.assertEqual(event_from_json.getName(), "Event1")
        self.assertEqual(event_from_json.getTimeStamp(), 1648226400.0)

    def test_setFields(self):
        event = OneTimeEvent()
        event.setFields("Event2", 1648302800.0)
        self.assertEqual(event.getName(), "Event2")
        self.assertEqual(event.getTimeStamp(), 1648302800.0)

    def test_toJson(self):
        event = OneTimeEvent()
        event.setFields("Event3", 1648389200.0)
        expected_json = '{"name": "Event3", "timeStamp": 1648389200.0}'
        self.assertEqual(json.loads(event.toJSON()), json.loads(expected_json))

    def test_eq(self):
        event1 = OneTimeEvent()
        event1.setFields("Event4", 1648475600.0)

        event2 = OneTimeEvent()
        event2.setFields("Event4", 1648475600.0)

        event3 = OneTimeEvent()
        event3.setFields("Event5", 1648475600.0)

        self.assertTrue(event1 == event2)
        self.assertFalse(event1 == event3)

    def test_hash(self):
        event1 = OneTimeEvent()
        event1.setFields("Event6", 1648562000.0)

        event2 = OneTimeEvent()
        event2.setFields("Event6", 1648562000.0)

        event3 = OneTimeEvent()
        event3.setFields("Event7", 1648562000.0)

        self.assertEqual(hash(event1), hash(event2))
        self.assertNotEqual(hash(event1), hash(event3))

if __name__ == '__main__':
    unittest.main()
