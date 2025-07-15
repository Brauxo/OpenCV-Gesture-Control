import cv2
import numpy as np
import time

from camera_manager import CameraManager
from hand_detector import HandDetector
from controller import SystemController
from gesture_manager import GestureManager
from config import AppConfig, Landmark, AppMode

def main():
    """The main function to run the hand tracking application."""
    try:
        #  init
        cfg = AppConfig()
        camera = CameraManager(width=cfg.CAM_WIDTH, height=cfg.CAM_HEIGHT)
        detector = HandDetector(max_hands=1)
        controller = SystemController()
        gesture_mgr = GestureManager()

        current_mouse_x, current_mouse_y = controller.screen_width / 2, controller.screen_height / 2
        prev_time = 0

        print("Educational Hand Tracking App - Started")

        # Main
        while True:
            # Capture
            success, frame = camera.get_frame()
            if not success: break
            
            # Detetct hands
            annotated_frame, all_hands = detector.process_frame(frame)
            
            mode_text = "INACTIVE"
            mode_color = (0, 0, 255)

            if all_hands:
                hand = all_hands[0]
                
                # gesture
                mode, mode_data = gesture_mgr.get_mode(hand)

                # Actions
                if mode == "navigate":
                    mode_text, mode_color = "NAVIGATE", (0, 255, 0)
                    
                    # 1. Move Mouse
                    anchor = hand[cfg.CURSOR_ANCHOR]
                    target_x = np.interp(anchor['x'], (cfg.FRAME_PADDING, camera.width - cfg.FRAME_PADDING), (0, controller.screen_width))
                    target_y = np.interp(anchor['y'], (cfg.FRAME_PADDING, camera.height - cfg.FRAME_PADDING), (0, controller.screen_height))
                    current_mouse_x += (target_x - current_mouse_x) * cfg.SMOOTHING
                    current_mouse_y += (target_y - current_mouse_y) * cfg.SMOOTHING
                    controller.move_mouse(current_mouse_x, current_mouse_y)
                    
                    # 2. Check for Clicks/Drags
                    action, action_data = gesture_mgr.get_action(hand)
                    if action == "left_click": 
                        controller.left_click() 
                        print(f"Left Click at {current_mouse_x}, {current_mouse_y}")
                    elif action == "right_click": 
                        controller.right_click()
                        print(f"Right Click at {current_mouse_x}, {current_mouse_y}")
                    elif action == "drag_start": 
                        controller.mouse_down()
                        print(f"Drag started at {current_mouse_x}, {current_mouse_y}")
                    elif action == "drag_end": 
                        controller.mouse_up()
                        print(f"Drag ended at {current_mouse_x}, {current_mouse_y}")

                elif mode == "scroll":
                    mode_text, mode_color = "SCROLL", cfg.SCROLL_MODE_COLOR
                    # Simple scroll based on hand height (not ideal but works for demo)
                    scroll_amount = -np.interp(hand[Landmark.WRIST]['y'], [camera.height * 0.2, camera.height * 0.8], [-10, 10])
                    controller.scroll(int(scroll_amount))
                    
                elif mode == "inactive":
                    mode_text, mode_color = "INACTIVE (Fist)", (0, 0, 255)

            # Visual Feedback
            fps = int(1 / (time.time() - prev_time)) if (time.time() - prev_time) > 0 else 0
            prev_time = time.time()
            cv2.putText(annotated_frame, f"FPS: {fps}", (10, 30), cfg.FONT, 1, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"MODE: {mode_text}", (10, 70), cfg.FONT, 1, mode_color, 2)
            cv2.imshow("Educational Hand Tracking", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'): break
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'camera' in locals(): camera.release()
        cv2.destroyAllWindows()
        print("Application closed.")

if __name__ == "__main__":
    main()