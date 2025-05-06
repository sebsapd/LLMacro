import time
import os
from multiprocessing import Process
from pynput import keyboard
from logic.utils import is_loop_fully_empty, get_scancode

class MacroRunner:
    def __init__(self, name, event_list, binded_action_key):
        self.name = name
        self.event_list = event_list
        self.binded_action_key = binded_action_key
        self.process = None
        self.execution_queue = []
        self.is_macro_running = False

    # function called upon macro execution
    def run(self):
        from ctypes import CDLL, WinDLL, c_int, c_bool

        # preparing the path to the custom library and loading it
        self.user32 = WinDLL('user32', use_last_error=True)
        dll_path = os.path.join(os.path.dirname(__file__), "sendInput.dll")
        self.lib = CDLL(dll_path)

        # configuring the function signature for send_input
        self.lib.send_input.argtypes = [c_int, c_bool]
        self.lib.send_input.restype = None

        self.execution_queue = self.create_execution_queue(self.event_list)

        # triggering events from the execution queue in a loop
        while True:
            try:
                for func in self.execution_queue:
                    func()
            except Exception as e:
                print(f"[MacroRunner:{self.name}] ERR in run(): {e}")
            time.sleep(0.01)  # time interval between event calls to prevent the loop from consuming 100% CPU

    # if the process does not exist or has stopped running,
    # it creates a new Process object from the multiprocessing module,
    # specifying self.run as the target function.
    def start_macro(self):
        if not self.process or not self.process.is_alive():
            self.process = Process(target=self.run)
            self.process.start() # starts a new parallel Python process and executes self.run() in it
            self.is_macro_running = True

    # kills the process, interrupting the macro
    def stop_macro(self):
        if self.process and self.process.is_alive():
            self.process.terminate() # sends a termination signal to the child process
            self.process.join() # waits until the process actually finishes
            self.is_macro_running = False

    def toggle_macro(self):
        if self.is_macro_running:
            self.stop_macro()
        else:
            self.start_macro()

    # creating execution queue
    def create_execution_queue(self, event_list):
        queue = []
        for event in event_list:
            match event["func"]:
                case "loop_event":
                    if not is_loop_fully_empty(event):
                        for _ in range(int(event["repeats"])):
                            loop_queue = []
                            loop_queue = self.create_execution_queue(event["events"])
                            queue.extend(loop_queue)

                case "key_event":
                    key = event["key"]
                    event_time = float(event["time"].replace(',', '.'))
                    queue.append(lambda key=key, event_time=event_time: self.simulate_key(get_scancode(key), event_time))

                case "wait_event":
                    event_time = float(event["time"].replace(',', '.'))
                    queue.append(lambda event_time=event_time: time.sleep(event_time))

                case "text_event":
                    text = event["text"]
                    queue.append(lambda text=text: self.type_text(text))

                case "mouse_button_event":
                    key = event["key"]
                    event_time = float(event["time"].replace(',', '.'))
                    queue.append(lambda key=key, event_time=event_time: self.simulate_key(get_scancode(key), event_time))
        return queue

    # function responsible for typing text
    def type_text(self, text):
        from ctypes import windll
        user32 = windll.user32
        for char in text:
            vk_code = user32.VkKeyScanA(ord(char)) & 0xFF
            scancode = user32.MapVirtualKeyA(vk_code, 0)
            self.simulate_key(scancode, 0.05)

    # function responsible for sending a key press
    def simulate_key(self, key, delay):
        from ctypes import CDLL
        dll_path = os.path.join(os.path.dirname(__file__), "sendInput.dll")
        lib = CDLL(dll_path)
        lib.send_input(key, False)
        time.sleep(delay)
        lib.send_input(key, True)
