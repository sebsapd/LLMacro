from logic.dataActions import DataActions
from logic.widgetActions import WidgetActions
from ui import KeyListWidget, LoopListWidget, WaitListWidget, TextListWidget

class AppController:
    def __init__(self, main_window):

        # connecting the main window
        self.main_window = main_window

        # connecting the main program functions
        self.widget_actions = WidgetActions(self)
        self.data_actions = DataActions(self)
        
        # connecting event list widgets
        self.keyListWidget = KeyListWidget(self)
        self.loopListWidget = LoopListWidget(self)
        self.waitListWidget = WaitListWidget(self)
        self.textListWidget = TextListWidget(self)