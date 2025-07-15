# Educational OpenCV-Gesture-Control (Hand Tracking Mouse)

This project is a reference implementation for a hand-tracking virtual mouse, designed for educational purposes. It demonstrates a clean architecture, robust gesture recognition, and clear configuration, making it an ideal starting point for anyone interested in computer vision and human-computer interaction.

## Features

-   **Mouse Movement:** Control the cursor by moving your hand.
-   **Left & Right Click:** Pinch with your index or middle finger.
-   **Drag & Drop:** Pinch and hold to start dragging.
-   **Scrolling Mode:** Make a "peace sign" to enter scroll mode.
-   **Pause Gesture:** Make a fist to temporarily pause all control.
-   **Extensible by Design:** Easily add new gestures and actions by modifying `config.py` and `gesture_manager.py`.

## Requirements

-   Python (between 3.8 - 3.11)
-   A webcam

The required Python libraries are listed in `requirements.txt`.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Brauxo/OpenCV-Gesture-Control
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Run the application:**
    ```bash
    python main.py
    ```

2.  **Gestures:**
    -   **Activate:** Show an open hand to the camera.
    -   **Pause:** Make a closed fist.
    -   **Move Cursor:** With an open hand, move the base of your index finger.
    -   **Left Click:** Briefly pinch your thumb and index finger.
    -   **Right Click:** Briefly pinch your thumb and middle finger.
    -   **Drag:** Pinch your thumb and index finger and hold.
    -   **Enter Scroll Mode:** Make a "peace sign" (✌️). Move your hand up/down to scroll.

## How to Customize

This project is designed to be easy to modify.

-   **To change any setting (smoothing, click sensitivity, colors):**
    Edit the values in `config.py`. All settings are in one place with descriptive comments.

-   **To add a new gesture:**
    1.  Add a new checking function (e.g., `_is_thumbs_up`) in `gesture_manager.py`.
    2.  Add it to the `get_mode` or `get_action` logic.
    3.  Define a new action for the `SystemController` if needed.