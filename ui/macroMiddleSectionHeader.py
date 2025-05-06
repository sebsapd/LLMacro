from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget
from logic.utils import get_key_name

class MiddleSectionHeader(QWidget):

    binded_key_changed = Signal(int)

    def __init__(self, macro_name = "", binded_key = None, total_time = None, parent=None):
        super().__init__(parent)
        self.macro_name = macro_name
        self.binded_key = binded_key
        self.total_time = total_time
        self.listening = False
        self.init_middle_section_header()

    # defining the widget's appearance - the UI will be separated from the logic in future updates
    def init_middle_section_header(self):

        self.setObjectName(u"middleSectionHeader")
        self.setFixedSize(QSize(450, 60))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # spacer
        self.horizontalLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        # label name
        self.label_name = QLabel(self)
        font = QFont()
        font.setFamilies([u"Titillium Web"])
        font.setPointSize(17)
        self.label_name.setFont(font)
        self.label_name.setStyleSheet(u"font-size: 17pt;")
        self.label_name.setText(self.macro_name)
        self.horizontalLayout.addWidget(self.label_name)
        
        # spacer
        self.horizontalLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        # V line
        self.line_7 = QFrame(self)
        self.line_7.setStyleSheet(u"background: #262626;")
        self.line_7.setLineWidth(2)
        self.line_7.setFrameShape(QFrame.Shape.VLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)
        self.horizontalLayout.addWidget(self.line_7)

        # spacer
        self.horizontalLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        # container 
        self.bindKeyContainer = QWidget(self)
        self.bindKeyContainer.setFixedSize(QSize(45, 60))

        self.verticalLayout_7 = QVBoxLayout(self.bindKeyContainer)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)

        # label binded key
        self.label_binded_key = QLabel(self.bindKeyContainer)
        self.label_binded_key.setFixedHeight(20)
        self.label_binded_key.setText("Bind")
        self.label_binded_key.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_binded_key.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_7.addWidget(self.label_binded_key)

        # button bind key
        self.button_bind_key = QPushButton(self.bindKeyContainer)
        self.button_bind_key.setFixedHeight(30)
        self.button_bind_key.setStyleSheet("background: #262626; border-radius: 0px;")

        if self.binded_key:
            self.button_bind_key.setText(get_key_name(self.binded_key))

        self.button_bind_key.clicked.connect(self.start_listening)

        self.verticalLayout_7.addWidget(self.button_bind_key)
        self.horizontalLayout.addWidget(self.bindKeyContainer)

        # spacer
        self.horizontalLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        # V line
        self.line_6 = QFrame(self)
        self.line_6.setStyleSheet(u"background: #262626;")
        self.line_6.setLineWidth(2)
        self.line_6.setFrameShape(QFrame.Shape.VLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)
        self.horizontalLayout.addWidget(self.line_6)

        # spacer
        self.horizontalLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        # label time
        self.label_time = QLabel(self)
        self.label_time.setStyleSheet(u"border-radius: 0px;")
        self.label_time.setText(str(self.total_time))
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.horizontalLayout.addWidget(self.label_time)

        # spacer
        self.horizontalLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        # SVG time
        self.widget_2 = QWidget(self)
        self.widget_2.setFixedSize(QSize(40, 40))
        self.widget_2.setStyleSheet(u"image: url(:/icons/icons/time.svg);")
        self.horizontalLayout.addWidget(self.widget_2)

        # spacer
        self.horizontalLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

    # updating time
    def update_time(self, time):
        self.label_time.setText(str(time))

    # start listening for key binding
    def start_listening(self):
        self.listening = True
        self.grabKeyboard()

    # updating the binded key
    def keyPressEvent(self, event):
        if self.listening:
            scancode = event.nativeScanCode()
            self.releaseKeyboard()

            self.listening = False
            self.binded_key = scancode
            
            self.button_bind_key.setText(get_key_name(self.binded_key))

            self.binded_key_changed.emit(self.binded_key)
        else:
            super().keyPressEvent(event)

