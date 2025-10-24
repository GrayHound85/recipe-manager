from PyQt6.QtWidgets import QPushButton, QWidget, QFrame, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class ComponentEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.document().contentsChanged.connect(self.adjust_height)
        
    def adjust_height(self):
        doc_height = self.document().size().height()
        self.setFixedHeight(int(doc_height + 20))  # Add some padding
        