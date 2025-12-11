import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class _ScalerSignnls(QObject):
    scale_changed = pyqtSignal()
    

class Scaler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, reference_dpi=96):
        if getattr(self, "_initialized", False):
            return
        self.reference_dpi = reference_dpi
        self.__user_scale = 1
        self.device_scale = 1
        self._widgets = []
        self.signals = _ScalerSignnls()
        self._initialized = True
  

    def set_user_scale(self, value):
        self.__user_scale = value
        self.update_all()

    def global_scale(self):
        return self.device_scale * self.__user_scale

    def scale_value(self, value):
        return int(value * self.global_scale())

    def register_widget(self, widget, width=None, height=None, font_size=None):
        self._widgets.append((widget, width, height, font_size))
        self.apply(widget, width, height, font_size)

    def apply(self, widget, width=None, height=None, font_size=None):
        if width: widget.setFixedWidth(self.scale_value(width))
        if height: widget.setFixedHeight(self.scale_value(height))
        if font_size:
            f = widget.font()
            f.setPointSize(self.scale_value(font_size))
            widget.setFont(f)

    def update_all(self):
        for w, width, height, font_size in self._widgets:
            self.apply(w, width, height, font_size)
