import cv2
import numpy as np

def remove_checkerboard(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    
    # Check if it has an alpha channel, if not add one
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Convert to grayscale to detect the checkerboard squares
    gray = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2GRAY)
    
    # Checkerboard typically has values around 190-210 (gray) and 255 (white)
    # Most board components are green, black, or metallic.
    
    # Create mask for the "checkerboard" which is usually light gray/white
    # We'll use a threshold to keep anything that is NOT close to white/light gray
    # Or better: keep anything that has "color" (Saturation > 0)
    hsv = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2HSV)
    lower_color = np.array([0, 10, 10]) # Any saturation/value means it's likely a component
    upper_color = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Morphological operations to clean up the mask
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)
    
    # Apply mask to alpha channel
    img[:, :, 3] = mask
    
    cv2.imwrite(output_path, img)

if __name__ == "__main__":
    import sys
    remove_checkerboard("assets/pcba_item.png", "assets/pcba_item_clean.png")
