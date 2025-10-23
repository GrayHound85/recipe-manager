from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from ui.ui_scaler import Scaler

class SettingsMenu(QFrame):
    toggle_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scaler = Scaler()

        self.scaler.register_widget(self, width=220, height=150)
        self.setObjectName("SettingsMenu")

        self.setWindowFlags(Qt.WindowType.Widget)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        self.setStyleSheet("""
            QFrame#SettingsMenu {
                background-color: #2e2e2e;
                color: white;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        self.setVisible(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ------ Settings header + close button ------ #
        hbox1 = QHBoxLayout()
        layout.addLayout(hbox1)
        settings_header = QLabel("Settings")
        self.scaler.register_widget(settings_header, font_size=18)
        hbox1.addWidget(settings_header)
        self.close_button = SettingsButton(self)
        hbox1.addWidget(self.close_button)
        self.close_button.clicked.connect(self.toggle_requested.emit)
        
        # ------ Scale slider ------ # 
        hbox2 = QHBoxLayout()
        layout.addLayout(hbox2)
        scale_lable = QLabel("UI Scale ")
        hbox2.addWidget(scale_lable, alignment=Qt.AlignmentFlag.AlignLeft)
        self.scale_percentage_lable = QLabel("100%")
        hbox2.addSpacing(1)
        hbox2.addWidget(self.scale_percentage_lable, alignment=Qt.AlignmentFlag.AlignRight)
        self.scaler.register_widget(self.scale_percentage_lable, font_size=14)
        self.scaler.register_widget(scale_lable, font_size=14)
        


        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(75, 150)
        self.scale_slider.setValue(int(self.scaler.global_scale() * 100))
        layout.addWidget(self.scale_slider)

        # ------ Connect signals ------ #
        self.scale_slider.valueChanged.connect(self.on_scale_changed)
    
    def on_scale_changed(self, value):
        scale = value / 100
        self.scaler.set_user_scale(scale)
        self.scale_percentage_lable.setText(f"{int(scale * 100)}%")
        self.scaler.signals.scale_changed.emit()
    

class SettingsButton(QPushButton):
    def __init__(self, settings_menu, parent=None):
        super().__init__(parent)
        
        self.menu = settings_menu
        self.setIcon(QIcon.fromTheme("preferences-system"))
        self.setFlat(True)
        Scaler().register_widget(self, width=32, height=32)
