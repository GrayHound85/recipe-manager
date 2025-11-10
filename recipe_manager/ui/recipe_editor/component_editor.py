from PyQt6.QtWidgets import QPushButton, QWidget, QFrame, QTextEdit, QVBoxLayout, QSizePolicy, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from ui.ui_scaler import Scaler

class ComponentEditor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
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
    def __init__(self):
        super().__init__()
        self.scaler = Scaler()

        # Create layouts
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(15,5,15,5)
        layout.setSpacing(5)
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
    
