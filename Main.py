import sys
from ctypes import *
from PySide6.QtWidgets import QApplication, QMainWindow
from ui import *
from logic.appController import AppController


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.macro_handler = []
        self.current_properties = None  # currently displayed properties
        self.current_widget = None  # currently selected KeyListWidget
        self.current_macro = None # currently selected macro
        self.current_macro_file_path = None # currently selected macro path
        self.current_macro_header = None # currently selected macro header

        # integrating Main.py with the main controller
        self.controller = AppController(self)
        self.widget_actions = self.controller.widget_actions
        self.data_actions = self.controller.data_actions


        #__________ ui buttons __________

        # left section
        self.ui.list_macro.itemClicked.connect(lambda item: self.widget_actions.on_macro_selected(item))
        self.ui.button_add_macro.clicked.connect(lambda: self.widget_actions.create_new_macro(self))
        #self.ui.button_macro_folder.clicked.connect()
        #self.ui.button_macro_options.clicked.connect()

        # middle section
        self.ui.list_event.itemClicked.connect(lambda item: self.widget_actions.on_event_selected(item))

        # right section
        self.ui.button_add_key.clicked.connect(lambda: self.widget_actions.add_event_to_list("key"))
        self.ui.button_add_wait.clicked.connect(lambda: self.widget_actions.add_event_to_list("wait"))
        self.ui.button_add_loop.clicked.connect(lambda:self.widget_actions.add_loop_to_list_button())
        self.ui.button_add_mouse_button.clicked.connect(lambda: self.widget_actions.add_event_to_list("mouse_button"))
        self.ui.button_add_type_text.clicked.connect(lambda: self.widget_actions.add_event_to_list("text"))

        # refreshing the macro list
        self.widget_actions.refresh_list_macro()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

    
