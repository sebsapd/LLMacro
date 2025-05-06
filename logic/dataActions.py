import json
from ui import KeyListWidget, LoopListWidget, TextListWidget, WaitListWidget, MouseButtonListWidget
from logic.utils import is_loop_fully_empty, total_time_counting

class DataActions:
    def __init__(self, controller):
        self.controller = controller
        self.main_window = self.controller.main_window

    # parsing data from a JSON file into the event list
    def parse_event_list(self, list_event, item_number = None, current_loop_id = None, loop_repeats = None):
        events_call_list = []
        total_time = 0
        if not item_number: item_number = 0

        while item_number < list_event.count():
            item = list_event.itemWidget(list_event.item(item_number))

            match item:
                case LoopListWidget():
                    if item.action == "start":
                        item_number += 1
                        loop_event_list, second_item_number, sub_total_time = self.parse_event_list(list_event, item_number, item.loop_id, float(item.label_repeat_number.text()) )
                        total_time += sub_total_time
                        item_number = int(second_item_number)
                        events_call_list.append({
                            "func": "loop_event",
                            "loop_id": item.loop_id,
                            "repeats": item.label_repeat_number.text(),
                            "events": loop_event_list
                        })

                    elif item.action == "stop" and item.loop_id == current_loop_id:
                        return events_call_list, (item_number - 1), total_time
                    else:
                        print(f"ERR: Unexpected loop stop id={item.loop_id}, expected={current_loop_id}")

                case KeyListWidget():
                    total_time = total_time_counting(total_time, item.label_event_time.text(), current_loop_id, loop_repeats)
                    events_call_list.append({
                        "func": "key_event",
                        "key": item.label_event_key.text(),
                        "time": item.label_event_time.text()
                    })

                case WaitListWidget():
                    total_time = total_time_counting(total_time, item.label_time.text(), current_loop_id, loop_repeats)
                    events_call_list.append({
                        "func": "wait_event",
                        "time": item.label_time.text()
                    })

                case TextListWidget():
                    events_call_list.append({
                        "func": "text_event",
                        "text": item.text
                    })

                case MouseButtonListWidget():
                    total_time = total_time_counting(total_time, item.label_event_time.text(), current_loop_id, loop_repeats)
                    events_call_list.append({
                        "func": "mouse_button_event",
                        "key": item.label_event_key.text(),
                        "time": item.label_event_time.text()
                    })

            item_number += 1
        self.main_window.current_macro.total_time = total_time
        return events_call_list, item_number

    # saving parsed event list to the currently selected macro event list
    def save_to_macro_event_list(self):
        self.main_window.current_macro.event_list, _ = self.parse_event_list(self.main_window.ui.list_event)

    # saving currently selected macro event list to a JSON file
    def save_macro_event_list_to_file(self):
        with open(self.main_window.current_macro_file_path, "w") as file:
            json.dump(self.main_window.current_macro.event_list, file, indent = 4)

    #saving parsed event list to the currently selected macro event list and JSON file
    def save_to_file_and_event_list(self):
        self.save_to_macro_event_list()
        self.save_macro_event_list_to_file()

    # loading macro data from a JSON file into the currently selected macro event list
    def load_macro_data_from_file(self):
        with open(self.main_window.current_macro_file_path, "r") as file:
            self.main_window.current_macro.event_list = json.load(file)

    # loading widgets in the event list from macro data
    def load_macro_event_list_from_data(self, data):
        for event in data:
            match event["func"]:
                case "loop_event":
                    self.controller.widget_actions.add_loop_to_list("start",event["loop_id"], event["repeats"])

                    if not is_loop_fully_empty(event):
                        self.load_macro_event_list_from_data(event["events"])

                    elif is_loop_fully_empty(event):
                        loop_event = event.get("events")
                                                        
                        for prop in loop_event:
                            empty_loop_id = prop.get("loop_id")
                            empty_loop_repeats = prop.get("repeats")
                            self.controller.widget_actions.add_loop_to_list("start",empty_loop_id, empty_loop_repeats)
                            self.controller.widget_actions.add_loop_to_list("stop",empty_loop_id)

                    self.controller.widget_actions.add_loop_to_list("stop",event["loop_id"])

                case "key_event":
                    self.controller.widget_actions.add_event_to_list("key", event["key"], event["time"])

                case "wait_event":
                    self.controller.widget_actions.add_event_to_list("wait", event["time"])

                case "text_event":
                    self.controller.widget_actions.add_event_to_list("text", event["text"])

                case "mouse_button_event":
                    self.controller.widget_actions.add_event_to_list("mouse_button", event["key"], event["time"])