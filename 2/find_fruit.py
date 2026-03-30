import time
import cv2
import mss
import numpy as np
import win32api, win32con, win32gui
import threading
import math
import keyboard
import sys
import ctypes

# ==========================================
# CRITICAL: DPI AWARENESS & ADMIN CHECK
# ==========================================
# This stops Windows from messing up your mouse coordinates
ctypes.windll.shcore.SetProcessDpiAwareness(1)

if not ctypes.windll.shell32.IsUserAnAdmin():
    print("❌ SYSTEM ERROR: YOU MUST RUN AS ADMINISTRATOR!")
    time.sleep(5)
    sys.exit()

# ==========================================
# CONFIGURATION
# ==========================================
screenWidth = win32api.GetSystemMetrics(0)
screenHeight = win32api.GetSystemMetrics(1)
WINDOW_NAME = 'TRUE_AIM_VISION'

# Full Screen Capture
GAME_ZONE = {'top': 0, 'left': 0, 'width': screenWidth, 'height': screenHeight}

BOMB_SAFE_DISTANCE = 150
MIN_FRUIT_AREA = 1800 

def moveMouse(x, y):
    # Precise absolute movement
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 
        int(x/screenWidth*65535.0), int(y/screenHeight*65535.0), 0, 0)

def slice_fruit(x, y):
    # 1. Move to just above the fruit
    moveMouse(x, y - 60)
    # 2. Press and HOLD
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.02) # Give the game time to register the contact
    
    # 3. Fast Swipe Down through the fruit
    steps = 10
    for i in range(steps):
        moveMouse(x, (y - 60) + (i * 12)) 
    
    # 4. Release
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

swipeThread = None
def canSwipe():
    return (swipeThread is None) or not swipeThread.is_alive()

# --- MONITOR SETUP ---
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME, 400, 225)
cv2.moveWindow(WINDOW_NAME, screenWidth - 410, 10)

def make_topmost():
    hwnd = win32gui.FindWindow(None, WINDOW_NAME)
    if hwnd: win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# ==========================================
# MAIN LOOP
# ==========================================
with mss.mss() as sct:
    print(f"🚀 AI v10 ONLINE | Targeting {screenWidth}x{screenHeight}")
    print("WATCH FOR GREEN CIRCLES - IF THEY APPEAR, THE MOUSE WILL MOVE.")

    while True:
        if keyboard.is_pressed('q'): break
        make_topmost()

        # 1. Capture
        img = np.array(sct.grab(GAME_ZONE))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 2. STATED FRUIT COLORS (STRICT)
        boundaries = [
            ([18, 185, 120], [35, 255, 255], MIN_FRUIT_AREA, "fruit"), 
            ([0, 195, 120], [10, 255, 255], MIN_FRUIT_AREA, "fruit"),  
            ([35, 160, 110], [90, 255, 255], MIN_FRUIT_AREA, "fruit"), 
            ([0, 0, 0], [180, 255, 50], 1100, "bomb")                 
        ]

        fruits, bombs = [], []

        for lower, upper, area, label in boundaries:
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for c in cnts:
                if cv2.contourArea(c) < area: continue
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cX = int(M["m10"]/M["m00"])
                    cY = int(M["m01"]/M["m00"]) # CORRECTED Y CALCULATION
                    
                    if label == "fruit":
                        fruits.append((cX, cY))
                        cv2.circle(img, (cX, cY), 45, (0, 255, 0), 4)
                    else:
                        bombs.append((cX, cY))
                        cv2.circle(img, (cX, cY), 80, (0, 0, 255), 2)

        # 3. Action
        if canSwipe() and fruits:
            # Sort by Y (hit the one that's about to fall first)
            fruits.sort(key=lambda x: x[1], reverse=True)
            
            for fx, fy in fruits:
                safe = True
                for bx, by in bombs:
                    if math.dist((fx, fy), (bx, by)) < BOMB_SAFE_DISTANCE:
                        safe = False; break
                
                if safe:
                    # Launch slice thread
                    swipeThread = threading.Thread(target=slice_fruit, args=(fx, fy))
                    swipeThread.start()
                    break

        cv2.imshow(WINDOW_NAME, img)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

cv2.destroyAllWindows()