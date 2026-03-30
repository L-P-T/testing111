import os
import csv
import time
from datetime import datetime
import numpy as np
import cv2
import mss
from pynput import keyboard

# =========================
# Configuration
# =========================
# This ensures it saves directly in your project folder
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(PROJECT_ROOT, "training_data")
META_PATH = os.path.join(PROJECT_ROOT, "meta.csv")

# Image Settings
IMG_EXT = "jpg"
JPG_QUALITY = 95 

# Capture Speed
INTERVAL_FPS = 5.0  # 5 photos per second

# Hotkeys
HOTKEY_SINGLE = keyboard.Key.f8   # Manual Shot
HOTKEY_TOGGLE = keyboard.Key.f9   # Auto Mode ON/OFF
HOTKEY_QUIT = keyboard.Key.esc    # Exit

# =========================
# Helpers
# =========================
def ensure_dirs():
    if not os.path.exists(IMG_DIR):
        print(f"[SETUP] Creating directory: {IMG_DIR}")
        os.makedirs(IMG_DIR, exist_ok=True)

def init_meta_csv():
    if not os.path.exists(META_PATH):
        with open(META_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["filename", "timestamp", "epoch_ms", "mode", "region"])

def get_roi_from_user():
    print("\n[INSTRUCTION] Please ensure the Fruit Ninja window is VISIBLE on screen.")
    print("[INSTRUCTION] Taking a snapshot for selection in 3 seconds...")
    time.sleep(3)

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img_full = np.array(sct.grab(monitor))
        img_bgr = cv2.cvtColor(img_full, cv2.COLOR_BGRA2BGR)

        print("[ACTION] Select the game region with your mouse and press ENTER.")
        print("[ACTION] To restart selection, press 'c'.")
        
        # This opens the selection window
        roi = cv2.selectROI("SELECT GAME REGION (Press Enter when done)", img_bgr, showCrosshair=True, fromCenter=False)
        cv2.destroyAllWindows()

        x, y, w, h = roi
        
        if w == 0 or h == 0:
            print("[ERROR] No region selected. Exiting.")
            exit()

        capture_region = {
            "top": monitor["top"] + y,
            "left": monitor["left"] + x,
            "width": w,
            "height": h
        }
        
        print(f"\n[LOCKED] Target Region: {capture_region}")
        return capture_region

def save_frame(frame_bgr, mode, region):
    ts_ms = int(time.time() * 1000)
    filename = f"fn_{ts_ms}.{IMG_EXT}"
    path = os.path.join(IMG_DIR, filename)

    cv2.imwrite(path, frame_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), JPG_QUALITY])

    with open(META_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            filename,
            datetime.utcnow().isoformat() + "Z",
            ts_ms,
            mode,
            f"{region['top']},{region['left']},{region['width']},{region['height']}"
        ])
    
    if mode == "manual":
        print(f"[SAVED] {filename} (Manual)")

# =========================
# Main Execution
# =========================
def main():
    ensure_dirs()
    init_meta_csv()

    target_region = get_roi_from_user()

    running = True
    interval_mode = False
    
    print("\n=== FRUIT NINJA DATA COLLECTOR READY ===")
    print(f"  [F8]  -> Capture Single Frame")
    print(f"  [F9]  -> START/STOP Auto-Capture")
    print(f"  [ESC] -> STOP SCRIPT")
    print("----------------------------------------")

    with mss.mss() as sct:
        last_interval_time = 0.0
        interval_period = 1.0 / INTERVAL_FPS

        def on_press(key):
            nonlocal running, interval_mode
            try:
                if key == HOTKEY_QUIT:
                    running = False
                    return False
                if key == HOTKEY_SINGLE:
                    frame = np.array(sct.grab(target_region))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    save_frame(frame, "manual", target_region)
                if key == HOTKEY_TOGGLE:
                    interval_mode = not interval_mode
                    status = "RECORDING" if interval_mode else "PAUSED"
                    print(f"\n[SYSTEM] Auto-Capture: {status}")
            except Exception as e:
                print(f"Error: {e}")

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        try:
            while running:
                if interval_mode:
                    now = time.time()
                    if (now - last_interval_time) >= interval_period:
                        last_interval_time = now
                        frame = np.array(sct.grab(target_region))
                        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                        save_frame(frame_bgr, "interval", target_region)
                        print(".", end="", flush=True) 
                
                time.sleep(0.01) 

        except KeyboardInterrupt:
            pass
        finally:
            listener.stop()
            print("\n[SYSTEM] Mission Complete. Data saved.")

if __name__ == "__main__":
    main()