from PyQt6.QtWidgets import QPushButton, QWidget, QFrame, QTextEdit, QVBoxLayout, QSizePolicy, QHBoxLayout, QLabel, QLayout, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from ui.ui_scaler import Scaler

class ComponentEditor(QWidget):
    titleChanged = pyqtSignal(int, str)

    def __init__(self, component_id):
        super().__init__()
        layout = QVBoxLayout(self)
        self.scaler = Scaler()
        
        self._id = component_id
        self.component_name = "No name set"

        # Component title
        self.component_title = QLineEdit()
        self.component_title.setReadOnly(True)
        self.component_title.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                color: white;
            }
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid #888
            }
        """)
        self.component_title.editingFinished.connect(self._on_editing_finished)
        self.component_title.installEventFilter(self)
        self.component_title.textChanged.connect(self._on_title_changed)
        #self.scaler.register_widget(self.component_title, font_size=16)

        # Main body text edit
        self.text_edit = QTextEdit()
        self.text_edit.document().contentsChanged.connect(self.adjust_height)
        self.text_edit.setFixedHeight(45)

        layout.addWidget(self.component_title)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
    def adjust_height(self):
        doc_height = self.text_edit.document().size().height()
        self.text_edit.setFixedHeight(int(doc_height + 20))
        self.updateGeometry()
    
    def eventFilter(self, obj, event):
        if obj == self.component_title and event.type() == event.Type.MouseButtonDblClick:
            self.component_title.setReadOnly(False)
            self.component_title.setFocus()
            return True
        return super().eventFilter(obj, event)

    def _on_editing_finished(self):
        # Revert to read-only after the user finishes editing (e.g., presses Enter or loses focus)
        self.component_title.setReadOnly(True)
    
    def _on_title_changed(self, text):
        if not self.component_title.isReadOnly():
            self.titleChanged.emit(self._id, text)
   

class ComponentManager(QWidget):
    # Signals
    addRequested = pyqtSignal()

    deleteRequested = pyqtSignal(int)

    renameRequested = pyqtSignal(int, str)

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
        new_row.renameRequested.connect(lambda comp_id, text: self.renameRequested.emit(comp_id, text))
        self.component_rows[id] = new_row

    def on_component_deleted(self, id):
        if id in self.component_rows.keys():
            row = self.component_rows.pop(id)
            self.component_list_layout.removeWidget(row)

    def update_row_label(self, component_id, new_text):
        if component_id in self.component_rows:
            row = self.component_rows[component_id]
            row.comp_name.blockSignals(True)
            row.set_label(new_text)
            row.comp_name.blockSignals(False)

        
    
class ComponentRow(QWidget):
    deleteRequested = pyqtSignal()
    renameRequested = pyqtSignal(int, str)

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

        self.comp_name = QLineEdit("Temp name")
        self.comp_name.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        self.comp_name.textChanged.connect(lambda text: self.renameRequested.emit(self._id, text))

        self.delete_comp_button = QPushButton() 
        self.delete_comp_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.delete_comp_button.clicked.connect(lambda: self.deleteRequested.emit())
        layout.addWidget(self.comp_name)
        layout.addWidget(self.delete_comp_button)

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value

    def set_label(self, text):
        self.comp_name.setText(text)