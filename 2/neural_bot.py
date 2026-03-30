import cv2
import mss
import numpy as np
from ultralytics import YOLO
import win32api, win32con
import time
import keyboard
import ctypes

# --- SYSTEM SETTINGS ---
ctypes.windll.shcore.SetProcessDpiAwareness(1)
sw, sh = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
model = YOLO("best.pt")
sct = mss.mss()
monitor = {"top": 0, "left": 0, "width": sw, "height": sh}

def execute_action(targets):
    if not targets: return

    # --- CASE A: SINGLE FRUIT (The Sniper Strike) ---
    if len(targets) == 1:
        tx, ty = targets[0]
        # Quick vertical flick
        win32api.SetCursorPos((tx, ty - 100))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        # Fast 5-step flick
        for i in range(5):
            win32api.SetCursorPos((tx, ty - 100 + (i * 40)))
            time.sleep(0.005)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    # --- CASE B: MULTIPLE FRUITS (The Combo Swipe) ---
    else:
        # Sort left-to-right to create a path
        targets.sort(key=lambda x: x[0])
        
        start_x, start_y = targets[0]
        win32api.SetCursorPos((start_x, start_y - 50))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        
        for (tx, ty) in targets:
            win32api.SetCursorPos((tx, ty))
            time.sleep(0.02) # Give the game time to see the line connecting the fruits
            
        last_x, last_y = targets[-1]
        win32api.SetCursorPos((last_x, last_y + 50))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

print("⚔️ v19 HYBRID BOT | Single + Combo Support")

while True:
    if keyboard.is_pressed('q'): break

    img = np.array(sct.grab(monitor))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # imgsz=320 is the "Secret Sauce" for speed
    results = model.predict(img, imgsz=320, conf=0.35, verbose=False)

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

    # EXECUTE IF FRUITS FOUND
    if fruits_in_frame:
        execute_action(fruits_in_frame)

    # Display (Optional: Comment out cv2.imshow for 20% more speed)
    cv2.imshow("AI_HYBRID_VISION", cv2.resize(img, (640, 360)))
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cv2.destroyAllWindows()