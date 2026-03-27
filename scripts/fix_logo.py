import cv2
import numpy as np

def make_logo_transparent(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Simple threshold: anything that is NOT white (the W) should be transparent
    # The W is white (255, 255, 255)
    lower_white = np.array([200, 200, 200, 255])
    upper_white = np.array([255, 255, 255, 255])
    
    mask = cv2.inRange(img, lower_white, upper_white)
    
    # Create new image
    new_img = np.zeros_like(img)
    new_img[mask > 0] = [255, 255, 255, 255] # White pixels
    
    cv2.imwrite(output_path, new_img)

if __name__ == "__main__":
    make_logo_transparent("assets/wasion-ltd--600.png", "assets/wasion_white.png")
