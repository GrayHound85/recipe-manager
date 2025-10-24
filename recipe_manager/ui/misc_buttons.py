from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon

from ui.ui_scaler import Scaler

class BackButton(QPushButton):
    def __init__(self):
        super().__init__()
        Scaler().register_widget(self, width=32, height=32)
        self.setObjectName("BackButton")
        self.setIcon(QIcon.fromTheme("preferences-system"))
        self.setFlat(True)
        self.setStyleSheet("""
            QPushButton#BackButton {
                    
                }
        """)