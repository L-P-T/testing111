import cv2
import mss
import numpy as np
from ultralytics import YOLO
import time
import keyboard
import json
import socket

# --- NETWORK ---
UDP_IP = "127.0.0.1" 
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# --- STORAGE ---
coordinates_log = []

# --- VISION ---
model = YOLO("best.pt")
sct = mss.mss()
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080} 

print("👁️ VISION NODE ONLINE | Press 'Q' to save coordinates.json")

try:
    while True:
        if keyboard.is_pressed('q'): break

        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        results = model.predict(img, imgsz=320, conf=0.45, verbose=False)

        current_frame = {"timestamp": time.time(), "detections": []}

        for r in results:
            for box in r.boxes:
                # SAFE LABELING
                label = model.names[int(box.cls)]
                
                # SAFE UNPACKING (Flattening prevents the "got 1" error)
                coords = box.xyxy.cpu().numpy().flatten()
                x1, y1, x2, y2 = coords

                cX, cY = int((x1 + x2) / 2), int((y1 + y2) / 2)

                current_frame["detections"].append({
                    "label": label,
                    "x": cX,
                    "y": cY
                })

                # Draw for your own eyes
                color = (0, 255, 0) if label == "fruit" else (0, 0, 255)
                cv2.circle(img, (cX, cY), 10, color, -1)

        if current_frame["detections"]:
            sock.sendto(json.dumps(current_frame).encode(), (UDP_IP, UDP_PORT))
            coordinates_log.append(current_frame)

        cv2.imshow("Vision", cv2.resize(img, (640, 360)))
        if cv2.waitKey(1) & 0xFF == ord('q'): break

finally:
    if coordinates_log:
        with open("coordinates.json", "w") as f:
            json.dump(coordinates_log, f, indent=4)
        print("✅ Data saved to coordinates.json")
    cv2.destroyAllWindows()