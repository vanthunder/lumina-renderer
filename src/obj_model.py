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

import numpy as np


class OBJModel:
    """
    Class to represent and load OBJ models.

    Attributes:
        vertices (list[list[float]]): List of vertices.
        normals (list[list[float]]): List of normals.
        faces (list[list[tuple[int, int]]]): List of faces with vertex and normal indices.
        material_color (list[float]): Material color in RGBA.
        has_normals (bool): Indicates if normals are available.
    """

    def __init__(self, filename: str = None):
        """
        Initialize the OBJModel.

        Args:
            filename (str, optional): Path to the OBJ file to load.
        """
        self.vertices = []
        self.normals = []
        self.faces = []
        self.material_color = [1.0, 1.0, 1.0, 1.0]
        self.has_normals = False

        if filename:
            self.load_obj(filename)

    def load_obj(self, filename: str) -> None:
        """
        Load an OBJ file.

        Args:
            filename (str): Path to the OBJ file.
        """
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):  # Vertex
                    parts = line.strip().split()
                    vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                    self.vertices.append(vertex)
                elif line.startswith('vn '):  # Normal
                    parts = line.strip().split()
                    normal = [float(parts[1]), float(parts[2]), float(parts[3])]
                    self.normals.append(normal)
                elif line.startswith('f '):  # Face
                    parts = line.strip().split()
                    face = []
                    for part in parts[1:]:
                        vals = part.split('/')
                        v_idx = int(vals[0]) - 1
                        n_idx = int(vals[2]) - 1 if len(vals) > 2 and vals[2] else None
                        face.append((v_idx, n_idx))
                    # Triangulate faces with more than 3 vertices
                    if len(face) > 3:
                        for i in range(1, len(face) - 1):
                            self.faces.append([face[0], face[i], face[i + 1]])
                    else:
                        self.faces.append(face)
        self.has_normals = len(self.normals) > 0

    def calculate_normals(self) -> None:
        """Calculate normals for the model if they are missing."""
        normal_dict = {}
        self.normals = []
        for face in self.faces:
            # Get vertices of the face
            v0 = np.array(self.vertices[face[0][0]])
            v1 = np.array(self.vertices[face[1][0]])
            v2 = np.array(self.vertices[face[2][0]])

            # Calculate normal
            normal = np.cross(v1 - v0, v2 - v0)
            normal = normal / np.linalg.norm(normal) if np.linalg.norm(normal) != 0 else normal

            # Add normal to list
            normal_idx = len(self.normals)
            self.normals.append(normal.tolist())

            # Update face with normal index
            for i in range(len(face)):
                face[i] = (face[i][0], normal_idx)

        self.has_normals = True

    @staticmethod
    def cube():
        """Create a simple cube model."""
        cube = OBJModel()
        # Define 8 vertices of the cube
        cube.vertices = [
            [-1.0, -1.0, -1.0],  # 0
            [1.0, -1.0, -1.0],   # 1
            [1.0, 1.0, -1.0],    # 2
            [-1.0, 1.0, -1.0],   # 3
            [-1.0, -1.0, 1.0],   # 4
            [1.0, -1.0, 1.0],    # 5
            [1.0, 1.0, 1.0],     # 6
            [-1.0, 1.0, 1.0],    # 7
        ]
        # Define faces with vertex indices (counter-clockwise order)
        cube.faces = [
            # Front face
            [(0, None), (1, None), (2, None)],
            [(0, None), (2, None), (3, None)],
            # Back face
            [(4, None), (6, None), (5, None)],
            [(4, None), (7, None), (6, None)],
            # Left face
            [(0, None), (3, None), (7, None)],
            [(0, None), (7, None), (4, None)],
            # Right face
            [(1, None), (5, None), (6, None)],
            [(1, None), (6, None), (2, None)],
            # Top face
            [(3, None), (2, None), (6, None)],
            [(3, None), (6, None), (7, None)],
            # Bottom face
            [(0, None), (4, None), (5, None)],
            [(0, None), (5, None), (1, None)],
        ]
        # Calculate normals for the cube
        cube.calculate_normals()
        return cube
