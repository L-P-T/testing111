import pyautogui
import time
import os

# This tells Python to save the file in the SAME FOLDER where this script is saved
current_folder = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_folder, "pro_slices.txt")

print(f"--- ⏺️ DATA COLLECTION MODE ---")
print(f"File will be saved to: {path}")
input("Press Enter, then switch to the game and play!")

recorded_data = []
print("RECORDING... (Press Ctrl+C when the game ends)")

try:
    while True:
        x, y = pyautogui.position()
        recorded_data.append(f"{x},{y}")
        
        # Keep track in the console
        print(f"Captured Position: {x}, {y}  ", end="\r") 
        
        time.sleep(0.02) 
except KeyboardInterrupt:
    print("\n\nStopping and saving data...")

# Save the data
try:
    with open(path, "w") as f:
        for line in recorded_data:
            f.write(line + "\n")
    print(f"✅ SUCCESS! File saved as 'pro_slices.txt' in your folder.")
    print(f"Total points captured: {len(recorded_data)}")
except Exception as e:
    print(f"❌ Error saving file: {e}")