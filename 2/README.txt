===========================================================
      FruitNinja Aimbot - Computer Vision (ROLE 2) - README
===========================================================


INSTALL THESE BEFORE RUNNING:
Type this in your terminal:
pip install ultralytics mss opencv-python numpy keyboard pillow screeninfo pyyaml bettercam pywin32

-----------------------------------------------------------
2. CORE FILES
-----------------------------------------------------------
* neural_bot.py   -> THE MAIN SLICER. Run this for live play.
* find_coords.py  -> Script used to get fruit/bomb locations.
* coordinates.json -> Data log for Roles 5 and 7 to test.
* best.pt         -> The AI model file (Must be in this folder).

-----------------------------------------------------------
3. PERFORMANCE & GAME MODES
-----------------------------------------------------------
I have tested this on different modes. For best results:
- ZEN and ARCADE modes work the BEST.
- CLASSIC mode is okay, but the darker screen effects 
  can sometimes lower the AI's accuracy.

-----------------------------------------------------------
4. FOR ROLE 5 (LOGIC) & ROLE 6 (CONTROLS)
-----------------------------------------------------------
- Connection: UDP Port 5005
- Coordinates: (0,0) is Top-Left. 
- Output: Center X and Center Y of every object.

-----------------------------------------------------------
5. ARCHIVE (DO NOT USE / DEFECTIVE)
-----------------------------------------------------------
Ignore these files! They are old tests or have bugs:
tempcoords.py, capture-tool.py, ultimate_slicer.py, 
fast_coords.py, capture_tool, analyse.py, collect_data.py


-----------------------------------------------------------
6. Reference & Dataset Tools
-----------------------------------------------------------
- fruitninja-model.pt --> A sample YOLO model sourced online. Use this as a reference or a backup if needed.
- fruits_ref.py --> The script required to run the 'fruitninja-model.pt' reference model.
- find_fruit.py --> Our initial "Slicer" logic created before the YOLO model was integrated.
- process_dataset.py --> The tool used to capture and organize screenshots for training.
- processed data --> Folder containing the output images from the dataset processor.
- gameplay videos--> Contains raw and sliced gameplay footage for model verification.

-----------------------------------------------------------
7. HOW TO RUN
-----------------------------------------------------------
1. Open Fruit Ninja.
2. Run "python neural_bot.py" in your terminal.
3. Press 'Q' to stop and save the logs.
===========================================================