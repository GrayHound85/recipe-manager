from PyQt6.QtWidgets import QPushButton, QWidget, QFrame, QTextEdit, QVBoxLayout, QSizePolicy, QHBoxLayout, QLabel, QLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from ui.ui_scaler import Scaler

class ComponentEditor(QWidget):
    def __init__(self, component_id):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self._id = component_id
        self.text_edit = QTextEdit()
        self.text_edit.document().contentsChanged.connect(self.adjust_height)
        self.text_edit.setFixedHeight(45)

        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
    def adjust_height(self):
        doc_height = self.text_edit.document().size().height()
        self.text_edit.setFixedHeight(int(doc_height + 20))
        self.updateGeometry()
    

class ComponentManager(QWidget):
    # Signals
    addRequested = pyqtSignal()

    deleteRequested = pyqtSignal(int)

    renameRequested = pyqtSignal(int)

    selectRequested = pyqtSignal(int)

    # Initialisation
    def __init__(self):
        super().__init__()
        self.scaler = Scaler()

        self.component_rows = {}

        # Create layouts
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(15,5,15,5)
        layout.setSpacing(5)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        # Style manager
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("ComponentManager")
        self.setStyleSheet("""
                           #ComponentManager {background: #454545; 
                           border-radius: 10px;}
                           """)

        # Manager content
        self.title_label = QLabel("Components")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scaler.register_widget(self.title_label, font_size=14)
        layout.addWidget(self.title_label)
        self.title_underline = QFrame()
        self.title_underline.setFrameShape(QFrame.Shape.HLine)
        self.title_underline.setStyleSheet("background: grey")
        self.scaler.register_widget(self.title_underline, height=2)
        layout.addWidget(self.title_underline)

        # Component row container
        self.component_list_container = QWidget()
        self.component_list_layout = QVBoxLayout(self.component_list_container)
        self.component_list_layout.setContentsMargins(0,0,0,0)
        self.component_list_layout.setSpacing(5)
        layout.addWidget(self.component_list_container)

        # Add component button logic
        def on_add_component():
            self.addRequested.emit()

        

        self.add_component_button = QPushButton()
        self.add_component_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.add_component_button.clicked.connect(on_add_component)
        layout.addWidget(self.add_component_button)

    def on_component_added(self, id):
        print(id)
        new_row = ComponentRow(id)
        self.component_list_layout.addWidget(new_row)

        new_row.deleteRequested.connect(lambda: self.deleteRequested.emit(id))
        self.component_rows[id] = new_row

    def on_component_deleted(self, id):
        if id in self.component_rows.keys():
            row = self.component_rows.pop(id)
            self.component_list_layout.removeWidget(row)


        
    
class ComponentRow(QWidget):
    deleteRequested =pyqtSignal()

    def __init__(self, id):
        super().__init__()

        self._id = id
        self.scaler = Scaler()

        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(2,2,2,2)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("ComponentRow")
        self.setStyleSheet("""
                           #ComponentRow {background: #404040; 
                           border-radius: 10px;}
                           """)

        self.comp_name_label = QLabel("Temp name")
        self.comp_name_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        self.delete_comp_button = QPushButton() 
        self.delete_comp_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.delete_comp_button.clicked.connect(lambda: self.deleteRequested.emit())
        layout.addWidget(self.comp_name_label)
        layout.addWidget(self.delete_comp_button)

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value

    def set_label(self, text):
        self.comp_name_label.setText(text)