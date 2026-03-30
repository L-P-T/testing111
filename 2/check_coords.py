import pyautogui
import time

print("🎯 CALIBRATION MODE")
print("Hover your mouse over the corners. Press Ctrl+C to stop.")

try:
    while True:
        # This shows the X and Y of your mouse in real-time
        x, y = pyautogui.position()
        print(f"Current Position: X={x}, Y={y}    ", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n✅ Calibration stopped.")