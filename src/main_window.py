"""
Copyright 2024 Marvin Schubert

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QColorDialog, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from src.gl_widget import GLWidget


class MainWindow(QMainWindow):
    """
    Main window class that contains the OpenGL widget and control buttons.
    """

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        self.setWindowTitle("Lumina Renderer")

        # Main container and layout
        self.container = QWidget()
        self.layout = QVBoxLayout()

        # Add OpenGL widget
        self.glWidget = GLWidget()
        self.glWidget.setMinimumSize(800, 450)
        self.layout.addWidget(self.glWidget)

        # Add buttons
        self.button_create_cube = QPushButton("Create Cube")
        self.button_load_obj = QPushButton("Load OBJ")
        self.button_change_material = QPushButton("Change Material Color")
        self.layout.addWidget(self.button_create_cube)
        self.layout.addWidget(self.button_load_obj)
        self.layout.addWidget(self.button_change_material)

        self.button_create_cube.clicked.connect(self.glWidget.addCube)
        self.button_load_obj.clicked.connect(self.loadObj)
        self.button_change_material.clicked.connect(self.changeMaterialColor)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Timer for animation
        self.timer_id = self.startTimer(16)  # ~60 FPS

    def loadObj(self) -> None:
        """Open file dialog to load an OBJ file."""
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Load OBJ", "", "OBJ Files (*.obj)", options=options
        )
        if fileName:
            self.glWidget.loadOBJ(fileName)

    def changeMaterialColor(self) -> None:
        """Open color picker to change the material color."""
        color = QColorDialog.getColor()
        if color.isValid():
            rgba = [color.redF(), color.greenF(), color.blueF(), color.alphaF()]
            self.glWidget.change_material_color(rgba)

    def timerEvent(self, event) -> None:
        """
        Update the scene for animation.

        Args:
            event (QTimerEvent): The timer event.
        """
        self.glWidget.animate()
