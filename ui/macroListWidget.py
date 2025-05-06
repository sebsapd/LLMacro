from pynput import keyboard
import keyboard

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from logic.macro import MacroRunner
from logic.utils import get_key_name

class MacroListWidget(QWidget):

    removalRequested = Signal()

    def __init__(self, file_name, parent=None):
        super().__init__(parent)
        self.file_name = file_name
        self.total_time = 0
        self.event_list = None
        self.state = False
        self.binded_action_key = None
        self.macro = None
        self.listening_state = False
        self._key_is_down = False 
        self.init_macro_list_widget()

    # defining the widget's appearance - the UI will be separated from the logic in future updates
    def init_macro_list_widget(self):
        self.setObjectName("MacroListWidget")
        self.setFixedSize(QSize(300, 80))
        self.setStyleSheet("font-size: 15pt;")

        # main layout
        self.main_widget = QHBoxLayout(self)
        self.main_widget.setSpacing(0)
        self.main_widget.setContentsMargins(0, 0, 0, 0)

        # spacer (main)
        self.main_widget.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        # label macro name
        self.label_macro_name = QLabel(self.file_name, self)
        self.label_macro_name.setEnabled(False)
        self.label_macro_name.setFixedWidth(140)
        self.main_widget.addWidget(self.label_macro_name)

        # spacer (main)
        self.main_widget.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # container for key:binded_key and is_active button
        self.widget = QWidget(self)
        self.widget.setFixedWidth(60)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # spacer (widget)
        self.verticalLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # container for key:binded_key
        self.widget_2 = QWidget(self.widget)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        # label binded key
        self.label_key_bind = QLabel(str(self.binded_action_key), self.widget_2)
        self.label_key_bind.setAlignment(Qt.AlignCenter)
        self.label_key_bind.setFixedSize(QSize(60, 20))
        self.horizontalLayout_2.addWidget(self.label_key_bind)

        self.verticalLayout.addWidget(self.widget_2)

        # button is_active
        self.button_is_active = QPushButton("OFF", self.widget)
        self.button_is_active.setFixedSize(QSize(60, 20))
        self.button_is_active.setStyleSheet("background: #f5485c")
        self.button_is_active.clicked.connect(lambda: self.start_stop_macro_button())

        self.verticalLayout.addWidget(self.button_is_active)

        # spacer (widget)
        self.verticalLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        self.main_widget.addWidget(self.widget)

        # spacer (main)
        self.main_widget.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))

        # button options
        self.button_macro_options = QPushButton("", self)
        self.button_macro_options.setFixedSize(QSize(40, 40))
        self.button_macro_options.setStyleSheet("image: url(:/icons/icons/3dots.svg);")
        self.button_macro_options.setIconSize(QSize(40, 40))
        self.main_widget.addWidget(self.button_macro_options)

        # spacer (main)
        self.spacer4 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.main_widget.addItem(self.spacer4)

    def handle_delete(self):
        self.removalRequested.emit()

    # defining the function for the macro off/on button
    def start_stop_macro_button(self):
        if not self.listening_state:
            self.listening_state = True
            self.start_listener()

            # changing the button appearance
            self.button_is_active.setStyleSheet("background: #4be894")
            self.button_is_active.setText("ON")

        else:
            self.listening_state = False
            keyboard.unhook_all()
            self.start_stop_macro()

            # changing the button appearance
            self.button_is_active.setStyleSheet("background: #f5485c")
            self.button_is_active.setText("OFF")

    # starting and stopping the macro
    def start_stop_macro(self):
        if not self.state:
            self.state = True
            self.macro = MacroRunner(self.file_name, self.event_list, self.binded_action_key)
            self.macro.start_macro()

        else:
            self.state = False
            self.macro.stop_macro()
    
    # starting the listener
    def start_listener(self):
        def on_key_event(event):
            # checking the scancode of the pressed key against the bound key's scancode
            if event.scan_code != self.binded_action_key:
                return

            # key press
            if event.event_type == 'down' and not self._key_is_down:
                self._key_is_down = True
                self.start_stop_macro()

            # key release - it will be upgraded in future updates
            elif event.event_type == 'up':
                self._key_is_down = False

        # we don't block the GUI, the hook runs in the background
        keyboard.hook(on_key_event)
        
    # changing the binded key
    def change_binded_key(self, binded_key):
        self.binded_action_key = binded_key
        self.label_key_bind.setText(get_key_name(self.binded_action_key))
        if self.state == True: self.start_stop_macro()
