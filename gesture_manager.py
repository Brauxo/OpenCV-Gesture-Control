import time
import numpy as np
from config import Landmark, AppConfig

class GestureManager:
    """
    Recognizes gestures from hand landmarks and determines the appropriate action.
    This class encapsulates all the complex gesture logic.
    """
    def __init__(self):
        self.cfg = AppConfig()
        self.last_click_time = 0
        self.pinch_start_time = 0
        self.is_dragging = False

    def _distance(self, p1, p2):
        return np.hypot(p1['x'] - p2['x'], p1['y'] - p2['y'])

    def _is_fist(self, hand):
        palm_center = hand[Landmark.MIDDLE_FINGER_MCP]
        for tip_id in [Landmark.INDEX_FINGER_TIP, Landmark.MIDDLE_FINGER_TIP, Landmark.RING_FINGER_TIP, Landmark.PINKY_TIP]:
            if self._distance(hand[tip_id], palm_center) > self.cfg.FIST_THRESH:
                return False
        return True

    def _is_peace_sign(self, hand):
        index_up = hand[Landmark.INDEX_FINGER_TIP]['y'] < hand[Landmark.INDEX_FINGER_PIP]['y']
        middle_up = hand[Landmark.MIDDLE_FINGER_TIP]['y'] < hand[Landmark.MIDDLE_FINGER_PIP]['y']
        ring_down = hand[Landmark.RING_FINGER_TIP]['y'] > hand[Landmark.RING_FINGER_MCP]['y']
        pinky_down = hand[Landmark.PINKY_TIP]['y'] > hand[Landmark.PINKY_MCP]['y']
        fingers_apart = self._distance(hand[Landmark.INDEX_FINGER_TIP], hand[Landmark.MIDDLE_FINGER_TIP]) > self.cfg.PEACE_SIGN_THRESH
        
        return index_up and middle_up and ring_down and pinky_down and fingers_apart

    def _is_shaka_sign(self, hand):
        """Checks for a 'shaka' or 'call me' sign for volume control."""
        thumb_up = hand[Landmark.THUMB_TIP]['x'] < hand[Landmark.THUMB_MCP]['x'] # Simple check for thumb out
        pinky_up = hand[Landmark.PINKY_TIP]['y'] < hand[Landmark.PINKY_PIP]['y']
        index_down = hand[Landmark.INDEX_FINGER_TIP]['y'] > hand[Landmark.INDEX_FINGER_MCP]['y']
        middle_down = hand[Landmark.MIDDLE_FINGER_TIP]['y'] > hand[Landmark.MIDDLE_FINGER_MCP]['y']
        
        return thumb_up and pinky_up and index_down and middle_down

    def get_mode(self, hand_landmarks):
        """Determines the current application mode based on a static gesture."""
        if self._is_fist(hand_landmarks):
            return "inactive", None
        if self._is_peace_sign(hand_landmarks):
            return "scroll", None
        return "navigate", None

    def get_action(self, hand_landmarks):
        """Recognizes dynamic actions like clicks and drags."""
        # Check for cooldown
        if (time.time() - self.last_click_time) < self.cfg.CLICK_COOLDOWN:
            return None, None

        thumb_tip = hand_landmarks[Landmark.THUMB_TIP]
        index_tip = hand_landmarks[Landmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks[Landmark.MIDDLE_FINGER_TIP]

        # Right Click (Thumb + Middle)
        if self._distance(thumb_tip, middle_tip) < self.cfg.RIGHT_CLICK_THRESH:
            self.last_click_time = time.time()
            return "right_click", None

        # Left Click & Drag Logic (Thumb + Index)
        is_pinching = self._distance(thumb_tip, index_tip) < self.cfg.LEFT_CLICK_THRESH
        
        if is_pinching:
            if not self.pinch_start_time:
                self.pinch_start_time = time.time()
            
            # If pinch held long enough, start drag
            if (time.time() - self.pinch_start_time > self.cfg.DRAG_START_TIME) and not self.is_dragging:
                self.is_dragging = True
                return "drag_start", None
        else:
            if self.pinch_start_time: # If pinch was just released
                if self.is_dragging:
                    self.is_dragging = False
                    return "drag_end", None
                else: # It was a short pinch, so it's a click
                    self.last_click_time = time.time()
                    self.pinch_start_time = 0
                    return "left_click", None
            self.pinch_start_time = 0
        
        return None, None