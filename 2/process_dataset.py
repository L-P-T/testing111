import cv2                              
import numpy as np
import os

def sample_color(frame, region)cd:
    left, upper, right, lower = region
    h, w = frame.shape[:2]
    left = max(0, left)
    upper = max(0, upper)
    right = min(w, right)
    lower = min(h, lower)
    
    y_delta = lower - upper
    x_delta = right - left
    
    if y_delta <= 0 or x_delta <= 0:
        return None
    
    dim_samples = 4
    y_step = max(1, y_delta // dim_samples)
    x_step = max(1, x_delta // dim_samples)
    
    roi = frame[upper:lower, left:right]
    if roi.size == 0:
        return None
    
    color_sum = np.array([0, 0, 0], dtype=np.float64)
    sampled = 0
    
    for y in range(0, roi.shape[0], y_step):
        for x in range(0, roi.shape[1], x_step):
            color_sum += roi[y, x].astype(np.float64)
            sampled += 1
    
    if sampled == 0:
        return None
    
    avg = (color_sum / sampled).astype(int)
    return [int(avg[0]), int(avg[1]), int(avg[2])]

def is_fruit_color(avg_color):
    if avg_color is None:
        return False
    
    b, g, r = avg_color
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    saturation = max_c - min_c
    brightness = max_c
    
    # Lower thresholds to catch darker fruits
    if saturation < 20:
        return False
    
    if brightness < 25:
        return False
    
    return True

def detect_fruits_and_bombs(image_path):
    frame = cv2.imread(image_path)
    if frame is None:
        return None
    
    frame = cv2.resize(frame, (750, 500))
    height, width = frame.shape[:2]
    
    # === ALL FRUIT COLORS ===
    # Yellow (banana, lemon)
    lower_yellow = np.array([15, 100, 150])
    upper_yellow = np.array([45, 255, 255])
    
    # Green (lime, watermelon outside)
    lower_green = np.array([25, 30, 30])
    upper_green = np.array([90, 255, 255])
    
    # Orange (orange, mango, peach)
    lower_orange = np.array([5, 80, 120])
    upper_orange = np.array([30, 255, 255])
    
    # Red (apple, strawberry)
    lower_red = np.array([0, 60, 50])
    upper_red = np.array([15, 255, 255])
    lower_red2 = np.array([165, 60, 50])
    upper_red2 = np.array([180, 255, 255])
    
    # Purple (plum, passion fruit)
    lower_purple = np.array([90, 40, 40])
    upper_purple = np.array([170, 255, 220])
    
    # Brown (coconut)
    lower_brown = np.array([5, 30, 30])
    upper_brown = np.array([30, 150, 150])
    
    # Dark green (kiwi)
    lower_dark_green = np.array([20, 20, 20])
    upper_dark_green = np.array([70, 150, 130])
    
    # Create masks
    mask_yellow = cv2.inRange(frame, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(frame, lower_green, upper_green)
    mask_orange = cv2.inRange(frame, lower_orange, upper_orange)
    mask_red1 = cv2.inRange(frame, lower_red, upper_red)
    mask_red2 = cv2.inRange(frame, lower_red2, upper_red2)
    mask_red = mask_red1 | mask_red2
    mask_purple = cv2.inRange(frame, lower_purple, upper_purple)
    mask_brown = cv2.inRange(frame, lower_brown, upper_brown)
    mask_dark_green = cv2.inRange(frame, lower_dark_green, upper_dark_green)
    
    # Combine all
    fruit_mask = (mask_yellow | mask_green | mask_orange | mask_red | 
                  mask_purple | mask_brown | mask_dark_green)
    
    # Bomb mask
    lower_bomb = np.array([0, 0, 0])
    upper_bomb = np.array([180, 60, 60])
    mask_bomb = cv2.inRange(frame, lower_bomb, upper_bomb)
    
    # Find contours
    contours, _ = cv2.findContours(fruit_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    fruits = []
    bombs = []
    
    for c in contours:
        if len(c) < 40:
            continue
        
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        
        if area < 1200 or area > 50000:
            continue
        
        avg_color = sample_color(frame, (x, y, x + w, y + h))
        
        if not is_fruit_color(avg_color):
            continue
        
        centerX = x + w // 2
        centerY = y + h // 2
        
        cv2.circle(frame, (centerX, centerY), 40, (0, 255, 0), 3)
        
        if 0 <= centerX < width and 0 <= centerY < height:
            if mask_bomb[centerY, centerX] > 0:
                bombs.append((centerX, centerY))
                continue
        
        fruits.append((centerX, centerY))
    
    return frame, fruits, bombs

def process_all(data_dir="training_data", output_dir="processed_data"):
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(data_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    print(f"Processing {len(files)} images...")
    
    fruit_count = 0
    
    for f in files:
        result, fruits, bombs = detect_fruits_and_bombs(os.path.join(data_dir, f))
        
        if result is not None:
            for bx, by in bombs:
                cv2.circle(result, (bx, by), 40, (0, 0, 255), 3)
            
            cv2.imwrite(os.path.join(output_dir, f"processed_{f}"), result)
            
            if len(fruits) > 0:
                  fruit_count += 1
    
    print(f"Done!")
    print(f"Images with fruits: {fruit_count}/{len(files)} ({fruit_count/len(files)*100:.1f}%)")

if __name__ == "__main__":
    process_all()