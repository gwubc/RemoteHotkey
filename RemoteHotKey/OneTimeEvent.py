import json


class OneTimeEvent:
    _name = None
    _timeStamp = None

    def __init__(self, data=None):
        if data is not None:
            if isinstance(data, str):
                data = json.loads(data)
            self.setFields(data.get("name", ""), data.get("timeStamp", 0))

    def setFields(self, name: str, timeStamp: float):
        self._name = name
        self._timeStamp = timeStamp

    def getName(self) -> str:
        return self._name

    def getTimeStamp(self) -> float:
        return self._timeStamp

    def toJSON(self):
        return json.dumps(self.toJSONDic())

    def toJSONDic(self):
        jsonDic = {"name": self._name, "timeStamp": self._timeStamp}
        return jsonDic

    def __eq__(self, o: object) -> bool:
        return o.__hash__() == self.__hash__()

    def __hash__(self) -> int:
        return hash(self._name + f"{self._timeStamp}")
