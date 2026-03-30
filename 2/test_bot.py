import cv2
import mss
import numpy as np
from ultralytics import YOLO
import win32api, win32con
import time
import keyboard
import ctypes

# --- YOUR ORIGINAL SETTINGS ---
ctypes.windll.shcore.SetProcessDpiAwareness(1)
sw, sh = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
model = YOLO("best.pt")
sct = mss.mss()
monitor = {"top": 0, "left": 0, "width": sw, "height": sh}

def execute_action(targets):
    if not targets:
        return
    
    # --- YOUR SINGLE FRUIT (UNCHANGED) ---
    if len(targets) == 1:
        tx, ty = targets[0]
        win32api.SetCursorPos((tx, ty - 100))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        for i in range(5):
            win32api.SetCursorPos((tx, ty - 100 + (i * 40)))
            time.sleep(0.005)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    # --- CLASSIC MULTI-FRUIT FIX (ONLY CHANGE) ---
    else:
        # 1. SORT Y THEN X (top-down natural swipe)
        targets.sort(key=lambda x: (x[1], x[0]))
        
        # 2. LONGER START/END (Classic needs more travel)
        first = targets[0]
        last = targets[-1]
        
        # Start HIGHER + LEFT
        win32api.SetCursorPos((first[0] - 80, first[1] - 120))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        
        # 3. FASTER swipe (Classic fruits move fast)
        for tx, ty in targets:
            win32api.SetCursorPos((tx, ty - 30))  # Aim above center
            time.sleep(0.01)  # WAS 0.02 → NOW 0.01
        
        # End LOWER + RIGHT  
        win32api.SetCursorPos((last[0] + 80, last[1] + 60))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

print("⚔️ YOUR CODE + 3 CLASSIC FIXES")
print("1. Sort Y→X  2. Longer path  3. Faster timing")

while True:
    if keyboard.is_pressed('q'):
        break
    
    # --- YOUR ORIGINAL DETECTION (CHANGED 1 LINE) ---
    img = np.array(sct.grab(monitor))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    results = model.predict(img, imgsz=416, conf=0.25, verbose=False)  # ↑416, ↓0.25
    
    fruits_in_frame = []
    for r in results:
        for box in r.boxes:
            label = model.names[int(box.cls[0])]
            x1, y1, x2, y2 = box.xyxy[0]
            cX, cY = int((x1 + x2) / 2), int((y1 + y2) / 2)
            
            if label == "fruit":
                fruits_in_frame.append((cX, cY))
                cv2.circle(img, (cX, cY), 20, (0, 255, 0), 2)
            elif label == "bomb":
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)
    
    if fruits_in_frame:
        execute_action(fruits_in_frame)
    
    cv2.imshow("YOUR_CODE_FIXED", cv2.resize(img, (640, 360)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()