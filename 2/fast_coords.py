import pyautogui
import time

# Let's test if the AI can hit the four corners of YOUR game
corners = [(147, 122), (1770, 122), (1770, 1000), (147, 1000)]

print("Switch to the game! Testing corners in 3 seconds...")
time.sleep(3)

for pt in corners:
    print(f"Moving to {pt}")
    pyautogui.moveTo(pt[0], pt[1], duration=0.5)
    time.sleep(0.5)