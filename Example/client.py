# Import necessary libraries and classes
import time
from RemoteHotKey.ClientManager import ClientManager
from RemoteHotKey.WebUI.Button import Button
from RemoteHotKey.State import State
from RemoteHotKey.OneTimeEvent import OneTimeEvent
from RemoteHotKey.WebUI.UITemplate import UIPage, UITemplate
from RemoteHotKey.ActionManager import ActionManager
from RemoteHotKey.Utility.ActionPerformer_Pynput import ActionPerformer_Pynput


# Define a custom button class that inherits from the Button class
class ExampleButton(Button):
    def __init__(self, name="", rowspan=1, colspan=1):
        super().__init__(name, name, rowspan=rowspan, colspan=colspan)

    # Update the state of the button when it is clicked
    def updateState(self, currentState: State, event) -> None:
        currentState.store(State.Keys.mostRecentUIElementId, self._identifier)
        currentState.store(f"{self._identifier}_ClickedTime",
                           currentState.getFromStorage(f"{self._identifier}_ClickedTime", 0) + 1)
        currentState.addOneTimeEvent(OneTimeEvent({"name": self._identifier}))
        return None


# Define a custom action manager class that inherits from ActionManager
class ExampleActionManager(ActionManager):
    def __init__(self):
        super().__init__()
        self.actionPerformer = ActionPerformer_Pynput()

    # Always start the one-time action
    def _shouldStartOneTimeAction(self) -> bool:
        return True

    def _oneTimeAction(self):
        print("ClientTime: ", time.time())
        print(self._currentState.getStorage())
        print([x.toJSONDic() for x in self._currentState.getEventLog()])
        for event in self._currentState.getEventLog():
            if event.getName() == "A":
                self.actionPerformer.rightClick()
            elif event.getName() == "B":
                self.actionPerformer.tapKeyboard("b")


# Create a client manager instance
client = ClientManager()

# Set up the UI template and add the custom buttons to the UI page
template = UITemplate("main")
page1 = UIPage((2, 2))
page1.addUIElement(ExampleButton("A"))
page1.addUIElement(ExampleButton("B"))
page1.addUIElement(ExampleButton("C"))
template.addPage(page1)

# Configure the client with the UI template and custom action manager
client.setUITemplate(template)
client.addActionManager(ExampleActionManager())

# Start the client and run the main loop
client.start()
print("Start")
while 1:
    time.sleep(10)
