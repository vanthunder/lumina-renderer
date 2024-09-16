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

from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import ctypes




class GLWidget(QOpenGLWidget):
    """
    OpenGL widget to render 3D models and handle user interactions.

    Attributes:
        object (OBJModel): The 3D model to render.
        angleX (float): Rotation angle around the X-axis.
        angleY (float): Rotation angle around the Y-axis.
        zoom (float): Zoom level for the camera.
        panX (float): Pan offset along the X-axis.
        panY (float): Pan offset along the Y-axis.
        lastPos (QPoint): Last position of the mouse for interaction.
        vertex_buffer (int): Vertex Buffer Object identifier.
        vertex_count (int): Number of vertices to draw.
        material_color (list[float]): The current material color in RGBA.
        enable_texture (bool): Whether textures should be enabled.
    """

    def __init__(self, parent=None):
        """
        Initialize the OpenGL widget.

        Args:
            parent (QWidget, optional): The parent widget.
        """
        super(GLWidget, self).__init__(parent)
        self.object = None
        self.angleX = 0.0
        self.angleY = 0.0
        self.zoom = -5.0
        self.panX = 0.0
        self.panY = 0.0
        self.lastPos = QPoint()
        self.vertex_buffer = None  # VBO identifier
        self.vertex_count = 0
        self.material_color = [1.0, 1.0, 1.0, 1.0]
        self.enable_texture = True

    def initializeGL(self) -> None:
        """Set up OpenGL settings."""
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_CULL_FACE)  # Enable if face culling is desired
        glShadeModel(GL_SMOOTH)
        glClearColor(0.1, 0.1, 0.1, 1.0)

        lightPos = [1.0, 1.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    def resizeGL(self, w: int, h: int) -> None:
        """
        Handle OpenGL resizing.

        Args:
            w (int): The new width of the widget.
            h (int): The new height of the widget.
        """
        h = h if h else 1  # Prevent division by zero
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self) -> None:
        """Render the OpenGL scene."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.panX, self.panY, self.zoom)
        glRotatef(self.angleX, 1.0, 0.0, 0.0)
        glRotatef(self.angleY, 0.0, 1.0, 0.0)

        # Set material color
        material_color = getattr(self.object, 'material_color', self.material_color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material_color)

        if self.vertex_buffer:
            # Bind the vertex buffer
            glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)

            # Enable client states
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_NORMAL_ARRAY)

            # Calculate stride and offsets
            stride = 6 * ctypes.sizeof(ctypes.c_float)  # 6 floats per vertex-normal pair
            vertex_offset = ctypes.c_void_p(0)
            normal_offset = ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float))

            # Set pointers
            glVertexPointer(3, GL_FLOAT, stride, vertex_offset)
            glNormalPointer(GL_FLOAT, stride, normal_offset)

            # Draw the arrays
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

            # Disable client states
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_NORMAL_ARRAY)

            # Unbind the buffer
            glBindBuffer(GL_ARRAY_BUFFER, 0)

    def loadOBJ(self, filename: str) -> None:
        """
        Load an OBJ model and initialize the vertex buffer.

        Args:
            filename (str): Path to the OBJ file.
        """
        from src.obj_model import OBJModel
        self.makeCurrent()  # Ensure OpenGL context is current
        self.delete_vbo()
        self.object = OBJModel(filename)
        if not self.object.has_normals:
            self.object.calculate_normals()  # Calculate normals if missing
        self.init_vbo()
        self.update()

    def addCube(self) -> None:
        """Create a simple cube and initialize the vertex buffer."""
        from src.obj_model import OBJModel
        self.makeCurrent()  # Ensure OpenGL context is current
        self.delete_vbo()
        self.object = OBJModel.cube()
        self.init_vbo()
        self.update()

    def init_vbo(self) -> None:
        """Initialize the vertex buffer object for faster rendering."""
        if self.object:
            data = []
            for face in self.object.faces:
                for idx, normal_idx in face:
                    vertex = self.object.vertices[idx]
                    normal = self.object.normals[normal_idx] if self.object.has_normals else [0.0, 0.0, 0.0]
                    data.extend(vertex + normal)

            data = np.array(data, dtype=np.float32)
            self.vertex_count = len(data) // 6  # 3 for vertex, 3 for normal

            # Generate and bind the vertex buffer
            self.vertex_buffer = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
            glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

    def delete_vbo(self) -> None:
        """Manually delete the vertex buffer to avoid memory leaks."""
        if self.vertex_buffer:
            self.makeCurrent()
            glDeleteBuffers(1, [self.vertex_buffer])
            self.vertex_buffer = None
            self.vertex_count = 0

    def mousePressEvent(self, event) -> None:
        """
        Handle mouse press event for interaction.

        Args:
            event (QMouseEvent): The mouse event.
        """
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event) -> None:
        """
        Handle mouse movement for rotating or panning.

        Args:
            event (QMouseEvent): The mouse event.
        """
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.RightButton:
            self.angleX += dy * 0.5
            self.angleY += dx * 0.5
        elif event.buttons() & Qt.MiddleButton:
            self.panX += dx * 0.01
            self.panY -= dy * 0.01

        self.lastPos = event.pos()
        self.update()

    def wheelEvent(self, event) -> None:
        """
        Handle mouse wheel for zooming.

        Args:
            event (QWheelEvent): The wheel event.
        """
        self.zoom += event.angleDelta().y() / 240.0
        self.update()

    def change_material_color(self, color: list[float]) -> None:
        """
        Change the material color.

        Args:
            color (list[float]): RGBA color values.
        """
        self.material_color = color
        self.update()

    def animate(self) -> None:
        """Animate the scene."""
        self.angleY += 0.5
        self.update()

    def closeEvent(self, event) -> None:
        """
        Handle widget close event.

        Args:
            event (QCloseEvent): The close event.
        """
        self.makeCurrent()
        self.delete_vbo()
        super().closeEvent(event)
