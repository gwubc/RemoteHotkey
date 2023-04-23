import unittest
import json
from RemoteHotKey.OneTimeEvent import OneTimeEvent
from RemoteHotKey.State import State


class StateTest(unittest.TestCase):

    def test_init(self):
        state = State()
        self.assertEqual(state.getFromStorage(State.Keys.currentPageIndex), 0)
        self.assertEqual(state.getEventLog(), [])

        json_data = '{"storage": {"State.Keys.currentPageIndex": 2}, "eventLog": [{"name": "Event1", "timeStamp": 1648226400.0}]}'
        state_from_json = State(json_data)
        self.assertEqual(state_from_json.getFromStorage(State.Keys.currentPageIndex), 2)
        self.assertEqual(len(state_from_json.getEventLog()), 1)

    def test_store_and_getFromStorage(self):
        state = State()
        state.store("key1", "value1")
        state.store("key2", 123)

        self.assertEqual(state.getFromStorage("key1"), "value1")
        self.assertEqual(state.getFromStorage("key2"), 123)
        self.assertIsNone(state.getFromStorage("key3"))
        self.assertEqual(state.getFromStorage("key3", "default_value"), "default_value")

    def test_getStorage(self):
        state = State()
        state.store("key1", "value1")
        state.store("key2", 123)

        storage = state.getStorage()
        self.assertEqual(storage["key1"], "value1")
        self.assertEqual(storage["key2"], 123)

    def test_addOneTimeEvent(self):
        state = State()
        event1 = OneTimeEvent()
        event1.setFields("Event1", 1648226400.0)

        state.addOneTimeEvent(event1)
        self.assertEqual(len(state.getEventLog()), 1)
        self.assertEqual(state.getEventLog()[0], event1)

    def test_toJsonDic(self):
        state = State()
        state.store("key1", "value1")
        state.store("key2", 123)
        event1 = OneTimeEvent()
        event1.setFields("Event1", 1648226400.0)
        state.addOneTimeEvent(event1)

        json_dic = state.toJsonDic()
        expected_json = '{"storage": {"key1": "value1", "key2": 123, "State.Keys.currentPageIndex": 0}, "eventLog": [{"name": "Event1", "timeStamp": 1648226400.0}]}'
        self.assertEqual(json.loads(json.dumps(json_dic)), json.loads(expected_json))

    def test_clearEventLog(self):
        state = State()
        event1 = OneTimeEvent()
        event1.setFields("Event1", 1648226400.0)
        state.addOneTimeEvent(event1)

        self.assertEqual(len(state.getEventLog()), 1)
        state.clearEventLog()
        self.assertEqual(len(state.getEventLog()), 0)

    def test_clearStorage(self):
        state = State()
        state.store("key1", "value1")
        state.store("key2", 123)

        self.assertEqual(len(state.getStorage()), 3) # Includes State.Keys.currentPageIndex
        state.clearStorage()
        self.assertEqual(len(state.getStorage()), 0)

if __name__ == '__main__':
    unittest.main()
