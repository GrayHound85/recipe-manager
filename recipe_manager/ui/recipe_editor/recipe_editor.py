from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QSizePolicy, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QFont

from ui.ui_scaler import Scaler
from ui.settings import SettingsMenu, SettingsButton
from ui.misc_buttons import BackButton
from ui.recipe_editor.component_editor import ComponentEditor, ComponentManager

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
        self.scroll_area = self._create_scroll_area()
        center_layout.addWidget(self.scroll_area, 1)

        main_layout.addLayout(center_layout)

        self.setLayout(main_layout)

    # ------------------------------------------------------------------- #
    #                         UI Components
    # ------------------------------------------------------------------- #
    # ------ Top bar ------ ------ #
    def _create_topbar(self):
        bar = QFrame()
        bar.setObjectName("TopBar")
        self.scaler.register_widget(bar, width=None, height=50)
        bar.setStyleSheet("""
            QFrame#TopBar {
                background-color: #6b6b6b;
            }
        """)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(5)
        # ------ Backbutton ------ #
        self.back_button = BackButton()
        layout.addWidget(self.back_button)

        # ------ Title ------ #
        title = QLineEdit("Recipe title")
        title.setStyleSheet("color: white;")
        self.scaler.register_widget(title, font_size=18)
        layout.addWidget(title)
        layout.addStretch(1)

        # ------ Saving status label ------ #
        self.saving_status_label = QLabel("Not saved")
        self.saving_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.saving_status_label.setStyleSheet("color: #8a8a8a")
        self.scaler.register_widget(self.saving_status_label, font_size=14)
        layout.addWidget(self.saving_status_label)
        layout.addStretch(1)

        # ------ Settings menu ------ #
        self.settings_menu = SettingsMenu(self)
        self.settings_button = SettingsButton(self.settings_menu, parent=bar)
        layout.addWidget(self.settings_button)

        def toggle_menu():
            if self.settings_menu.isVisible():
                self.settings_menu.hide()
                return

            # Anchor to top-right corner of parent window
            x = self.width() - self.settings_menu.width() - 10  # 10px padding from right
            y = 10  # 10px padding from top

            self.settings_menu.move(x, y)
            self.settings_menu.raise_()
            self.settings_menu.show()

        self.scaler.signals.scale_changed.connect(self.reposition_settings_menu)
        self.settings_button.clicked.connect(toggle_menu)
        self.settings_menu.toggle_requested.connect(toggle_menu)

        return bar
    
    # ------ More settings menu logic ------ #
    def reposition_settings_menu(self):
        if not self.settings_menu.isVisible():
            return

        # Keep anchored to top-right of main window
        x = self.width() - self.settings_menu.width() - 10
        y = 10
        self.settings_menu.move(x, y)
        self.settings_menu.raise_()

    
    # ------ Sidebar ------ ------ #
    def _create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        self.scaler.register_widget(sidebar, width=250, height=None)
        sidebar.setStyleSheet("""
            QFrame#Sidebar {
                background-color: #383838;
            }
        """)
        # Create layouts
        main_layout = QVBoxLayout(sidebar)
        sidebar_scroll_area = QScrollArea()
        sidebar_scroll_area.setContentsMargins(10,10,10,10)
        sidebar_scroll_area.setStyleSheet("background: transparent; border: none")
        main_layout.addWidget(sidebar_scroll_area)
        layout = QVBoxLayout(sidebar_scroll_area)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        component_manager = ComponentManager()
        layout.addWidget(component_manager)


        return sidebar


    # ------ Scroll area ------ ------ #
    def _create_scroll_area(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("background-color: #2e2e2e;")

        # ------ Content widget ------ #
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content_layout.setContentsMargins(0, 20, 0, 20)
        scroll_area.setWidget(content_widget)

        # ------ Page ------ #
        page_frame = QFrame()
        page_frame.setFixedWidth(1000)
        page_frame.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        page_frame.setObjectName("Page")
        page_frame.setStyleSheet("""
            QFrame#Page {
                background-color: #383838;
                border-radius: 8px;
            }
        """)
        content_layout.addWidget(page_frame)

        page_layout = QVBoxLayout(page_frame)
        page_layout.setContentsMargins(20,20,20,20)
        page_layout.setSpacing(10)
        page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
        base_component_editor = ComponentEditor()
        page_layout.addWidget(base_component_editor)
        
        return scroll_area