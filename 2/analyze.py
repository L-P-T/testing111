# Open the file and read the numbers
with open("pro_slices.txt", "r") as f:
    lines = f.readlines()

y_coords = []

for line in lines:
    if "," in line:
        # Split the X and Y, and convert Y to a number
        parts = line.split(",")
        y_val = int(parts[1].strip())
        y_coords.append(y_val)

if y_coords:
    # Find the boundaries
    lowest_y = min(y_coords)  # The highest point on screen
    highest_y = max(y_coords) # The lowest point on screen
    
    print(f"--- 📊 PRO DATA ANALYSIS ---")
    print(f"Your Top Limit (Lowest Y): {lowest_y}")
    print(f"Your Bottom Limit (Highest Y): {highest_y}")
    print(f"The 'Action Zone' height is: {highest_y - lowest_y} pixels.")
else:
    print("No data found in the file!")