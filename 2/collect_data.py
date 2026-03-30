import cv2
import numpy as np
import bettercam
import pygetwindow as gw
import os
import time

# Create a folder for Role 4
if not os.path.exists('training_data'):
    os.makedirs('training_data')

camera = bettercam.create(output_color="BGR")
camera.start(target_fps=30) # Lower FPS to avoid saving 1000 images in a second

def get_game_coords():
    try:
        win = [w for w in gw.getWindowsWithTitle('Fruit') if w.visible][0]
        return (win.left, win.top, win.right, win.bottom)
    except: return None

print("DATA COLLECTOR ACTIVE!")
print("Press 's' to save a manual snapshot or just let it run.")

img_count = 0

while True:
    frame = camera.get_latest_frame()
    coords = get_game_coords()
    
    if frame is not None and coords:
        left, top, right, bottom = coords
        game_area = frame[max(0,top):min(1080,bottom), max(0,left):min(1920,right)]
        
        if game_area.size > 0:
            # Simple red detection to 'trigger' a save
            hsv = cv2.cvtColor(game_area, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, np.array([0, 150, 50]), np.array([10, 255, 255]))
            
            # If we see a big white blob (fruit), save the RAW image for Role 4
            if np.sum(mask) > 10000:
                img_name = f"training_data/fruit_{int(time.time())}_{img_count}.jpg"
                cv2.imwrite(img_name, game_area)
                img_count += 1
                print(f"Saved image {img_count}")
                time.sleep(0.5) # Don't spam the hard drive!

            cv2.imshow("Collecting Data for Role 4", game_area)

    if cv2.waitKey(1) & 0xFF == ord('q') or img_count > 100:
        break

camera.stop()
cv2.destroyAllWindows()
print(f"Done! Send the 'training_data' folder to Role 4.")