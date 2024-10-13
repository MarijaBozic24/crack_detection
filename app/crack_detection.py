import cv2
import numpy as np
import uuid
import os


output_dir = 'outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def preprocess_image(image):
 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    img_log = (np.log(blur + 1) / (np.log(1 + np.max(blur)))) * 255
    img_log = np.array(img_log, dtype=np.uint8)

    bilateral = cv2.bilateralFilter(img_log, 5, 30, 30)

    edges = cv2.Canny(bilateral, 20, 80)

    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
  
    preprocessed_filename = f"preprocessed_{str(uuid.uuid4())[:8]}.png"
    preprocessed_path = os.path.join(output_dir, preprocessed_filename)
    cv2.imwrite(preprocessed_path, closing)

    return closing

def process_crack_image(image):
    
    image_id = str(uuid.uuid4())

   
    preprocessed_image = preprocess_image(image)
    contours, _ = cv2.findContours(preprocessed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cracks = []
    total_length = 0
    min_contour_length = 50  

    for idx, contour in enumerate(contours):
        length = cv2.arcLength(contour, False)

    
        if length < min_contour_length:
            continue

       
        x_start, y_start = contour[0][0]
        x_end, y_end = contour[-1][0]

        crack_label = f"Crack_{idx}" 

        cracks.append({
            'name': crack_label,
            'x_start': int(x_start),
            'y_start': int(y_start),
            'x_end': int(x_end),
            'y_end': int(y_end),
            'length': length,
            'image_id': image_id 
        })
        total_length += length

    return {
        'image_id': image_id,
        'crack_count': len(cracks),
        'cracks': cracks,
        'total_length': total_length,
        'preprocessed_image': preprocessed_image
    }


