import pyautogui
import platform
import subprocess

class SystemController:
    """Handles all interactions with the operating system."""
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.screen_width, self.screen_height = pyautogui.size()

    def move_mouse(self, x, y):
        pyautogui.moveTo(x, y, duration=0)

    def left_click(self):
        pyautogui.click(button='left')

    def right_click(self):
        pyautogui.click(button='right')
        
    def mouse_down(self):
        pyautogui.mouseDown(button='left')

    def mouse_up(self):
        pyautogui.mouseUp(button='left')

    def scroll(self, amount):
        pyautogui.scroll(amount)
