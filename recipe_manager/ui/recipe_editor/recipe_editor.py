from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ui.ui_scaler import Scaler

class RecipeEditor(QWidget):
    backendRequested = pyqtSignal()
    saveRequested = pyqtSignal()

    addComponentRequested = pyqtSignal()
    addStepRequested = pyqtSignal()
    insertImageRequested = pyqtSignal()


    def __init__(self, parent = None):
        super().__init__(parent)
        self.current_recipe_name: str = ""
        self.is_saved: bool = False
        self.scaler = Scaler()
        self._setup_ui()
    
            
    def connect_scale(self, update_func):
        self.scaler.scale_changed.connect(update_func)
        update_func()


    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- Top bar --- #
        top_bar = self._create_topbar()
        main_layout.addWidget(top_bar)

        # --- Main area --- #
        center_layout = QHBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        # --- Side bar --- #
        self.sidebar = self._create_sidebar()
        center_layout.addWidget(self.sidebar)

        # --- Scrollable editor area --- #
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.content_widget)

        center_layout.addWidget(self.scroll_area, 1)

        main_layout.addLayout(center_layout)

        self.setLayout(main_layout)

    # ------------------------------------------------------------------- #
    #                         UI Components
    # ------------------------------------------------------------------- #
    def _create_topbar(self):
        bar = QFrame()
        bar.setObjectName("TopBar")
        self.scaler.register_widget(bar, width=None, height=50)
        bar.setStyleSheet("""
            QFrame#TopBar {
                background-color: #6b6b6b;
            }
        """)

        return bar
    

    def _create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        self.scaler.register_widget(sidebar, width=150, height=None)
        sidebar.setStyleSheet("""
            QFrame#Sidebar {
                background-color: #383838;
            }
        """)


        return sidebar