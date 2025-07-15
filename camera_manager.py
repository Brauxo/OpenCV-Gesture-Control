import cv2

class CameraManager:
    """
    Manages the webcam feed.
    """
    def __init__(self, device_index=0, width=640, height=480):
        """
        Args:
            device_index (int): The index of the camera device to use.
            width (int): The desired width of the camera frame.
            height (int): The desired height of the camera frame.
        """
        self.cap = cv2.VideoCapture(device_index)
        if not self.cap.isOpened():
            raise IOError(f"Cannot open webcam at index {device_index}")

        # Resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Get the actual frame dim
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Webcam initialized. Requested {width}x{height}, got {self.width}x{self.height}")

    def get_frame(self):
        """
        Reads a single frame from the webcam.
        """
        success, frame = self.cap.read()
        if not success:
            return False, None
        return True, cv2.flip(frame, 1)

    def release(self):
        """
        Releases the webcam resource.
        """
        self.cap.release()
        print("Webcam released.")