import os
from ui import *

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QListWidgetItem, QWidget, QVBoxLayout
from ui.macroMiddleSectionHeader import MiddleSectionHeader

class WidgetActions:

    def __init__(self, controller):
        self.controller = controller
        self.main_window = self.controller.main_window
        self.current_macro = self.main_window.current_macro

# _____________________ LIST MACRO _____________________
   
   # selecting a macro to focus
    def on_macro_selected(self, item):
        # saving the event list state when switching macros
        if not self.main_window.current_macro == None:
            self.controller.data_actions.save_to_macro_event_list()
            self.controller.data_actions.save_macro_event_list_to_file()

        self.main_window.current_macro = self.main_window.ui.list_macro.itemWidget(item)
        self.main_window.current_macro_file_path = f"macros/{self.main_window.current_macro.file_name}.json"

        self.change_header_in_main_section() # updating the header with data of the selected macro
        self.clear_properties() # clearing properties widget
        self.refresh_list_event() # refreshing the event list to display those contained in the current macro

    # refreshing the macro list
    def refresh_list_macro(self):
        for i in range(self.main_window.ui.list_macro.count()):
            item = self.main_window.ui.list_macro.item(i)
            self.delete_widget_on_list(self.main_window.ui.list_macro, item)

        for file in os.listdir("macros"):
            self.add_macro_to_list(file)

    # adding an existing macro file to the macro list
    def add_macro_to_list(self, file):
        if file.endswith(".json"):
            file_name = os.path.splitext(file)[0]

            macro_list_widget = MacroListWidget(str(file_name))
            macro_item = QListWidgetItem(self.main_window.ui.list_macro)
            macro_item.setSizeHint(QSize(300,80))

            self.main_window.ui.list_macro.addItem(macro_item)
            self.main_window.ui.list_macro.setItemWidget(macro_item, macro_list_widget)

            macro_list_widget.removalRequested.connect(
                lambda lw=self.main_window.ui.list_macro, it=macro_item:
                self.main_window.delete_widget_on_list(lw, it))

    # creating new macro
    def create_new_macro(self, action = None):
        file_number = 0
        for f in os.listdir("macros"):
            file_number += 1

        while True:
            if not os.path.exists(f"macros/new_macro{file_number}.json"):
                with open(f"macros/new_macro{file_number}.json", 'w') as file:
                    file.write("")
                self.add_macro_to_list(f"new_macro{file_number}.json")
                
                return 0
            else: file_number += 1

# _____________________ LIST EVENT _____________________

    # selecting an event to focus and creating a properties widget for it
    def on_event_selected(self, item):
        # retrieving the widget associated with the item
        opened_event = self.main_window.ui.list_event.itemWidget(item)

        self.clear_properties() # clearing properties widget

        # matching selected widget
        match opened_event:
            case LoopListWidget():
                if opened_event.action == "start":
                    properties_widget = PropertiesLoop(opened_event.repeats)
                    properties_widget.properties_updated.connect(opened_event.update_repeat_number)
                else:
                    return

            case KeyListWidget():
                properties_widget = PropertiesKey(opened_event.key, opened_event.time)
                properties_widget.properties_updated.connect(opened_event.update_key_and_time)

            case WaitListWidget():
                properties_widget = PropertiesWait(opened_event.time)
                properties_widget.properties_updated.connect(opened_event.update_time)

            case TextListWidget():
                properties_widget = PropertiesText(opened_event.text)
                properties_widget.properties_updated.connect(opened_event.update_text)

            case MouseButtonListWidget():
                properties_widget = PropertiesMouseButton(opened_event.key, opened_event.time)
                properties_widget.properties_updated.connect(opened_event.update_key_and_time)

            case _:
                print("ERR: on_event_selected -> match opened_event")

        self.add_properties_to_container(properties_widget)

    # adding an event to the event list
    def add_event_to_list(self, event, prop_1 = "", prop_2 = ""):
        if self.main_window.current_macro:
            if event == "key": event_widget = KeyListWidget(self.controller, prop_1, prop_2)
            elif event == "wait": event_widget = WaitListWidget(self.controller, prop_1)
            elif event == "text": event_widget = TextListWidget(self.controller, prop_1)
            elif event == "mouse_button": event_widget = MouseButtonListWidget(self.controller, prop_1, prop_2)

            else:
                print("ERR: add_event_to_list")
                return
                            
            event_item = QListWidgetItem(self.main_window.ui.list_event)  
            event_item.setSizeHint(QSize(450,50))
            self.main_window.ui.list_event.addItem(event_item)
            self.main_window.ui.list_event.setItemWidget(event_item, event_widget)

            event_widget.removalRequested.connect(
                lambda list_widget=self.main_window.ui.list_event, item=event_item:
                self.delete_widget_on_list(list_widget, item))

    # creating an ID for the loop
    def create_loop_id(self):
        loop_id = 1 
        instances = 0
        for i in range (self.main_window.ui.list_event.count()):
            event = self.main_window.ui.list_event.itemWidget(self.main_window.ui.list_event.item(i))
            if isinstance(event, LoopListWidget): instances += 1
        if instances >= 2: loop_id = int(instances / 2) + 1
        return loop_id

    # user adding a loop event to the list
    def add_loop_to_list_button(self):
        loop_id = self.create_loop_id()
        self.add_loop_to_list("start", loop_id)
        self.add_loop_to_list("stop", loop_id)

    # adding a loop event to the list
    def add_loop_to_list(self, start_or_stop, loop_id, repeats = ""):
            if start_or_stop == "start": event_widget = LoopListWidget(self.controller, loop_id, start_or_stop, repeats)
            elif start_or_stop == "stop": event_widget = LoopListWidget(self.controller, loop_id, start_or_stop)

            event_item = QListWidgetItem(self.main_window.ui.list_event)  
            event_item.setSizeHint(QSize(450,50))
            self.main_window.ui.list_event.addItem(event_item)
            self.main_window.ui.list_event.setItemWidget(event_item, event_widget)

            event_widget.removalRequested.connect(
                lambda list_widget=self.main_window.ui.list_event, item=event_item:
                self.delete_widget_on_list(list_widget, item))

    # refreshing the list event widget
    def refresh_list_event(self):
        for i in reversed (range(self.main_window.ui.list_event.count())):
            item = self.main_window.ui.list_event.item(i)
            self.delete_widget_on_list(self.main_window.ui.list_event, item)

        self.controller.data_actions.load_macro_data_from_file()
        self.controller.data_actions.load_macro_event_list_from_data(self.main_window.current_macro.event_list)

# _____________________ EVENT PROPERTIES _____________________

    # adding a properties widget for the selected event
    def add_properties_to_container(self, properties_widget):
         # check if the layout already exists
        if self.main_window.ui.widget_properties.layout() is None:
            main_layout = QVBoxLayout(self.main_window.ui.widget_properties)
            main_layout.setContentsMargins(0, 0, 0, 0)
        else:
            main_layout = self.main_window.ui.widget_properties.layout()
            # clear previous widgets
            while main_layout.count():
                item = main_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        main_layout.addWidget(properties_widget)
        self.main_window.current_properties = properties_widget

    # clear properties widget
    def clear_properties(self):
        for child in self.main_window.ui.widget_properties.findChildren(QWidget):
            child.deleteLater()
        self.main_window.current_properties = None

# _____________________ OTHER _____________________

    # remove the widget from the list
    def delete_widget_on_list(self, list_widget, item):
        widget = list_widget.itemWidget(item)

        if widget is None: return

        # check if the widget has a loop_id
        loop_id = getattr(widget, "loop_id", None)

        # remove the main widget from the list
        row = list_widget.row(item)
        list_widget.takeItem(row)
        widget.deleteLater()

        if loop_id is None: return
        
        # search for and remove other widgets with the same loop_id
        for i in reversed(range(list_widget.count())):
            other_item = list_widget.item(i)
            other_widget = list_widget.itemWidget(other_item)

            if other_widget is None:
                continue

            # check if another widget also has the same loop_id
            other_loop_id = getattr(other_widget, "loop_id", None)

            if other_loop_id == loop_id:
                list_widget.takeItem(i)
                other_widget.deleteLater()

    # updating the header with data of the selected macro
    def change_header_in_main_section(self):
        layout = self.main_window.ui.header_holder.layout()
        if layout is not None and layout.count() > 0:
            layout.itemAt(0).widget().deleteLater()

        file_name = self.main_window.current_macro.file_name
        total_time = self.main_window.current_macro.total_time
        binded_action_key = self.main_window.current_macro.binded_action_key

        widget = MiddleSectionHeader(file_name, binded_action_key, total_time)

        widget.binded_key_changed.connect(self.main_window.current_macro.change_binded_key)

        self.main_window.ui.header_holder.layout().addWidget(widget)
        self.main_window.current_macro_header = widget














