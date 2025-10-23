from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSlider, QLabel, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

from ui.ui_scaler import Scaler

class SettingsMenu(QFrame):
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
        
        # ------ Scale slider ------ # 
        scale_lable = QLabel("UI Scale ")
        self.scaler.register_widget(scale_lable, font_size=14)
        layout.addWidget(scale_lable)

        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(75, 150)
        self.scale_slider.setValue(int(self.scaler.global_scale() * 100))
        layout.addWidget(self.scale_slider)

        # ------ Connect signals ------ #
        self.scale_slider.valueChanged.connect(self.on_scale_changed)
    
    def on_scale_changed(self, value):
        scale = value / 100
        self.scaler.set_user_scale(scale)
        self.scaler.signals.scale_changed.emit()
    

class SettingsButton(QPushButton):
    def __init__(self, settings_menu, parent=None):
        super().__init__(parent)
        
        self.menu = settings_menu
        self.setIcon(QIcon.fromTheme("preferences-system"))
        self.setFlat(True)
        Scaler().register_widget(self, width=32, height=32)
