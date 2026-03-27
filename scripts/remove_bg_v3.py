import cv2
import numpy as np

def remove_background(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None: return
    # Convert to RGBA
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # White background threshold
    white_bins = np.all(img[:, :, :3] > 245, axis=-1)
    img[white_bins, 3] = 0
    
    cv2.imwrite(output_path, img)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        remove_background(sys.argv[1], sys.argv[2])
