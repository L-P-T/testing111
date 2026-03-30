import pyautogui

print("Move mouse to top-left of game window, then press Enter")
input()
x1, y1 = pyautogui.position()
print(f"Top-left: {x1}, {y1}")

print("Move mouse to bottom-right of game window, then press Enter")
input()
x2, y2 = pyautogui.position()
print(f"Bottom-right: {x2}, {y2}")

print(f"\nWidth: {x2 - x1}, Height: {y2 - y1}")
print(f"Set GAME_SCREEN = {{'top': {y1}, 'left': {x1}, 'width': {x2-x1}, 'height': {y2-y1}}}")