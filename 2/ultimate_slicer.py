import cv2
import numpy as np
import bettercam
import time
import pydirectinput
import ctypes

# This tells Windows to look at the screen exactly as it is (no scaling)
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# YOUR VERIFIED SETTINGS
X_START, Y_START = 147, 122
GAME_REGION = (X_START, Y_START, 1770, 1000)

camera = bettercam.create(region=GAME_REGION)
pydirectinput.PAUSE = 0 

print("--- ⚔️ ULTIMATE SAFE SLICER ACTIVE ⚔️ ---")

try:
    while True:
        frame = camera.grab()
        if frame is not None:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Mask the background
            lower_wood = np.array([0, 40, 40])
            upper_wood = np.array([30, 255, 255])
            wood_mask = cv2.inRange(hsv, lower_wood, upper_wood)
            fruit_mask = cv2.bitwise_not(wood_mask)
            
            contours, _ = cv2.findContours(fruit_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # GAME OVER PROTECTION: If the screen is too messy, stop clicking
            if len(contours) > 15:
                time.sleep(2)
                continue

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if 1200 < area < 9000: 
                    M = cv2.moments(cnt)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"]) + X_START
                        cY = int(M["m01"] / M["m00"]) + Y_START
                        
                        # Only slice in the "Human" zone we found in your data
                        if 250 < cY < 850:
                            # The Human Slash
                            pydirectinput.moveTo(cX - 60, cY + 60)
                            pydirectinput.mouseDown()
                            pydirectinput.moveTo(cX + 160, cY - 160)
                            pydirectinput.mouseUp()
                            print(f"🎯 Sliced! Area: {int(area)}")
                            break 
        
        time.sleep(0.001)

except KeyboardInterrupt:
    print("\n[!] Stopping safely.")