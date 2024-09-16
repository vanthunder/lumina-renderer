
# Lumina Renderer

Lumina Renderer is an open-source, feature-rich 3D rendering engine built using PyQt5 and OpenGL. It supports rendering OBJ models, cube generation, material and texture customization, and interactive user controls. Designed with flexibility and scalability in mind, Lumina Renderer is suitable for educational purposes, game development, and various other applications.

## Features
- **OBJ Model Support**: Load and render 3D models from OBJ files with support for materials and textures.
- **Cube Generation**: Quickly generate 3D cubes for testing and prototyping.
- **Interactive Controls**: Mouse controls for rotating, zooming, and panning the camera view.
- **Material Customization**: Use a color picker to customize materials on the fly.
- **Performance Optimizations**: Leveraging OpenGL Vertex Buffer Objects (VBOs) for efficient rendering.
- **Extensible Design**: Easily extend the renderer with more features or customize it for specific use cases.
- **Animation Support**: Basic animation capabilities to animate models within the scene.

## Project Structure

```
lumina-renderer/
│
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── main.py               # Entry point of the application
├── assets/
│   └── models/           # Sample OBJ models for testing
└── src/
    ├── __init__.py       # Package initialization
    ├── gl_widget.py      # OpenGL widget for rendering
    ├── main_window.py    # Main application window
    └── obj_model.py      # OBJ model loading and processing
```

## Installation

### Prerequisites
- Python 3.6 or higher
- Pip package manager

### Steps

1. Clone the repository:

```bash
git clone https://github.com/vanthunder/lumina-renderer.git
cd lumina-renderer
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

## Usage

### User Interface
- **Create Cube**: Click the "Create Cube" button to generate and display a simple 3D cube.
- **Load OBJ**: Click the "Load OBJ" button to open a file dialog and select an OBJ file to load and render.
- **Change Material Color**: Click the "Change Material Color" button to open a color picker and change the material color of the model.

### Mouse Controls
- **Rotate Model**: Click and drag with the right mouse button to rotate the model around the X and Y axes.
- **Pan View**: Click and drag with the middle mouse button (or scroll wheel) to pan the view horizontally and vertically.
- **Zoom In/Out**: Use the mouse wheel to zoom in and out of the scene.

### Keyboard Shortcuts
- **Esc**: Close the application.

## Examples

### Loading an OBJ Model
- Click on the "Load OBJ" button.
- Navigate to the `assets/models/` directory or any directory containing your OBJ files.
- Select the desired OBJ file and click "Open".
- The model will be loaded and displayed in the OpenGL widget.

### Changing Material Color
- Click on the "Change Material Color" button.
- Use the color picker dialog to select a new color.
- Click "OK" to apply the color to the model.

## Development

### Project Setup
Ensure that the project structure is maintained as shown above. The `src` directory contains the main application modules:

- `gl_widget.py`: Contains the GLWidget class, responsible for rendering the 3D scene using OpenGL.
- `main_window.py`: Contains the MainWindow class, which sets up the main application window and user interface.
- `obj_model.py`: Contains the OBJModel class, which handles loading and parsing of OBJ files.

### Dependencies
The project relies on the following Python packages:
- **PyQt5**: For the GUI components and window management.
- **PyOpenGL**: To access OpenGL functions for rendering.
- **NumPy**: For efficient numerical computations, particularly when handling vertex data.

These are specified in the `requirements.txt` file:

```
PyQt5>=5.15.0
PyOpenGL>=3.1.5
NumPy>=1.19.0
```

### Running the Application
You can run the application using the `main.py` script:

```bash
python main.py
```

## Code Overview

### `main.py`
The entry point of the application. It initializes the PyQt application and displays the main window.

### `main_window.py`
Defines the MainWindow class, which sets up the user interface, including buttons and the OpenGL widget. It handles user interactions and events.

### `gl_widget.py`
Defines the GLWidget class, which is a subclass of QOpenGLWidget. It handles all OpenGL rendering, including initializing the OpenGL context, rendering the scene, and responding to user input for interaction.

### `obj_model.py`
Defines the OBJModel class, responsible for loading and parsing OBJ files. It handles vertices, normals, and faces, and provides functionality to generate a cube model.

## Troubleshooting

### Common Issues
- **ImportError**: If you encounter import errors related to PyQt5 or PyOpenGL, ensure that the packages are installed correctly and match the versions specified in `requirements.txt`.
- **OpenGL Errors**: If the application reports OpenGL errors, ensure that your system's graphics drivers are up to date and support the required OpenGL version.
- **Model Rendering Issues**: If models are not rendering correctly (e.g., missing faces), check the OBJ files for correctness. The renderer expects faces to be defined in a counter-clockwise order.

### Debugging Tips
- **Enable Face Culling**: Uncomment `glEnable(GL_CULL_FACE)` in `initializeGL()` to enable face culling, which can help identify issues with face winding.
- **OpenGL Error Checking**: Add `glGetError()` calls after OpenGL functions to check for errors.
- **Logging**: Use Python's logging module to add debug statements and track the application's state.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository on GitHub.
2. Clone your forked repository:

```bash
git clone https://github.com/vanthunder/lumina-renderer.git
cd lumina-renderer
```

3. Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
```

4. Make your changes to the codebase.
5. Commit your changes with descriptive messages:

```bash
git commit -am 'Add new feature: description of feature'
```

6. Push your branch to GitHub:

```bash
git push origin feature/your-feature-name
```

7. Open a pull request on the main repository.
8. Describe your changes in detail and submit the pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- **PyQt5**: For providing a powerful set of tools for creating GUIs in Python.
- **PyOpenGL**: For making OpenGL accessible in Python applications.
- **NumPy**: For efficient numerical computations.

## Contact
For questions, suggestions, or issues, please open an issue on the GitHub repository or contact the maintainers directly.
