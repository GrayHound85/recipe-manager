from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QSize
from ui.recipe_editor.recipe_editor import RecipeEditor
import sys

app = QApplication(sys.argv)

editor = RecipeEditor()
editor.setWindowTitle("Recipe Manager")
editor.setMinimumSize(1000, 600)
editor.show()

sys.exit(app.exec())