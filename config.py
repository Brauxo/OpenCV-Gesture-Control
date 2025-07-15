import cv2
from enum import Enum, IntEnum

class Landmark(IntEnum):
    """Enum for MediaPipe's 21 hand landmarks for readability."""
    WRIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_FINGER_MCP = 5
    INDEX_FINGER_PIP = 6
    INDEX_FINGER_DIP = 7
    INDEX_FINGER_TIP = 8
    MIDDLE_FINGER_MCP = 9
    MIDDLE_FINGER_PIP = 10
    MIDDLE_FINGER_DIP = 11
    MIDDLE_FINGER_TIP = 12
    RING_FINGER_MCP = 13
    RING_FINGER_PIP = 14
    RING_FINGER_DIP = 15
    RING_FINGER_TIP = 16
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20

class AppMode(Enum):
    """Enum for the application's current operational mode."""
    NAVIGATE = 1
    SCROLL = 2
    VOLUME_CONTROL = 3
    INACTIVE = 4

class AppConfig:
    #=================================
    # Camera and Performance
    #=================================
    CAM_WIDTH, CAM_HEIGHT = 640, 480
    TARGET_FPS = 60  
    ROI_PADDING = 50  
    DETECTION_INTERVAL = 3  

    #=================================
    # Mouse Control 
    #=================================
    CURSOR_ANCHOR = Landmark.INDEX_FINGER_MCP
    SMOOTHING = 0.2
    FRAME_PADDING = 100

    #=================================
    # Gesture Recognition and Definition
    #=================================
    # Pinch Thresholds (distance in pixels)
    LEFT_CLICK_THRESH = 30
    RIGHT_CLICK_THRESH = 35

    # Timing (in seconds)
    CLICK_COOLDOWN = 0.4
    DRAG_START_TIME = 0.15 # Hold pinch this long to start a drag

    # Fist: All finger tips must be closer than this to the palm center
    FIST_THRESH = 65
    
    # Peace Sign: Distance between index and middle tips for scroll mode
    PEACE_SIGN_THRESH = 30

    #=================================
    # Visual Feedback
    #=================================
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    CLICK_FEEDBACK_COLOR = (0, 255, 0)
    DRAG_FEEDBACK_COLOR = (0, 0, 255)
    SCROLL_MODE_COLOR = (255, 255, 0)
    VOLUME_MODE_COLOR = (255, 0, 255)