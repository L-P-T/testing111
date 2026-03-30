import os
import cv2
import numpy as np
from ultralytics import YOLO

class FruitNinjaDetector:

    def __init__(self, model_path=r"runs\detect\train2\weights\best.onnx"):

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"[CRITICAL ERROR] Deployment failed. Model not found at: {model_path}")
        
        print("[SYSTEM] Initializing Fruit Ninja AI Engine...")

        self.model = YOLO(model_path, task='detect')
        print("[SYSTEM] AI Engine Ready. Optimal Input Resolution: 320x320")

    def detect_objects(self, frame_bgr):
        
        results = self.model(frame_bgr, imgsz=320, verbose=False)
        
        detected_items = []
        for r in results:
            boxes = r.boxes
            for box in boxes:

                coords = box.xyxy[0].tolist() 
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                detected_items.append({
                    "x1": int(coords[0]),
                    "y1": int(coords[1]),
                    "x2": int(coords[2]),
                    "y2": int(coords[3]),
                    "class_id": class_id,
                    "confidence": confidence
                })
                
        return detected_items

if __name__ == "__main__":
    print("--- DEPLOYMENT SYSTEM TEST ---")
    detector = FruitNinjaDetector()
    
    dummy_frame = np.random.randint(0, 255, (600, 800, 3), dtype=np.uint8)
    
    import time
    start = time.time()
    results = detector.detect_objects(dummy_frame)
    end = time.time()
    
    print(f"Test Inference Time: {(end - start) * 1000:.2f} ms")
    print(f"Detected Items Output Format: {results}")
    print("--- SYSTEM READY FOR HANDOFF ---")