# Capture and refocusing an unstructured lightfield

By taking a video of a scene while varying the X-Y position of the camera, you create an unstructured lightfield of the scene. Using this unstructured lightfield, it's possible generate images with different focal points in the scene. This is done via a template matching algorithm.

### unstructuredlightfield.py
To run, modify the main() caller with your parameters of choice
The parameters are as follows:
- rubiks: Refocus on the Rubik's cube
- tea: Refocus on the green tea box
- mouse: Refocus on the computer mouse

The size of the template for all above refocuses is 60x60, which can be modified by setting twidth in the main() function appropriately. The size of the search window is defined as the last parameter of the refocus() function in this file, which can be set by changing the argument in the refocus caller in the main() function.

## Data
Capture an unstructured lightfield:
- IMG_1857.mov: The unstructured lightfield video. The code uses every 5 frames starting at frame 5.

Refocusing an unstructured lightfield:
- rubiks.png: Unstructured lightfield focused on the Rubik's cube
- tea.png: Unstructured lightfield focused on the green tea box
- mouse.png: Unstructured lightfield focused on the computer mouse
