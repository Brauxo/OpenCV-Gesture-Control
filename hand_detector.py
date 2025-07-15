import cv2
import mediapipe as mp

class HandDetector:
    """
    Finds hands in an image and returns their landmark data.
    """
    def __init__(self, max_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        """
        Args:
            max_hands (int): Maximum number of hands to detect.
            min_detection_confidence (float): Minimum confidence value for hand detection.
            min_tracking_confidence (float): Minimum confidence value for hand tracking.
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process_frame(self, frame):
        """
        Processes a single frame to find hands.
        Args:
            frame: The image frame from OpenCV.
        Returns:
            tuple: (annotated_frame, landmark_list)
                   'annotated_frame' has the landmarks drawn on it.
                   'landmark_list' contains the structured data for each detected hand.
        """
        # mediapipe need RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the frame and find hands
        self.results = self.hands.process(rgb_frame)
        
        annotated_frame = frame.copy()
        all_hands_landmarks = []

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # Draw landmarks on the frame for visualization
                self.mp_draw.draw_landmarks(
                    annotated_frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

                # Extract and store landmark data
                my_hand = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    # lm.x, lm.y are normalized coordinates (0 to 1)
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    my_hand.append({"id": id, "x": cx, "y": cy, "z": lm.z})
                all_hands_landmarks.append(my_hand)

        return annotated_frame, all_hands_landmarks