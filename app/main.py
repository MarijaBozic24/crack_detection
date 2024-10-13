from flask import Flask, request, jsonify
from crack_detection import process_crack_image
from crack_detection import preprocess_image
from models import CrackDetails, db
from database import insert_crack_coordinates, insert_crack_summary
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import cv2
import numpy as np 
import os
from matplotlib import pyplot as plt
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)



db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'  # Update with your database credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)


if not os.path.exists('outputs'):
    os.makedirs('outputs')

def combine_images(original_image, processed_image):
    """
    Combine the original image and the processed crack image.
    This will overlay the cracks on top of the original image for better visualization.
    """

    if original_image.shape != processed_image.shape:
        processed_image = cv2.resize(processed_image, (original_image.shape[1], original_image.shape[0]))


    if len(processed_image.shape) == 2:  
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)

    
    alpha = 0.7  # transparency for the original image
    beta = 0.3   # transparency for the processed crack image
    combined_image = cv2.addWeighted(original_image, alpha, processed_image, beta, 0)

    return combined_image
def draw_cracks_on_image(preprocessed_image):
    
    orb = cv2.ORB_create(nfeatures=1500)

    # Detect keypoints
    keypoints, descriptors = orb.detectAndCompute(preprocessed_image, None)

   
    featured_img = cv2.drawKeypoints(preprocessed_image, keypoints, None, color=(0, 255, 0))

    # Return the image with keypoints drawn
    return featured_img




@app.route('/process-crack', methods=['POST'])
def process_crack():
   
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image_file = request.files['image']

    # Decode the uploaded image
    image_bytes = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR) 

  
    if image is None:
        return jsonify({'error': 'Invalid image format'}), 400

 
    cracks_info = process_crack_image(image)

    session = Session()

    crack_coordinates = []

    for crack in cracks_info['cracks']:
        coordinates_id = insert_crack_coordinates(
            crack['x_start'],
            crack['y_start'],
            crack['x_end'],
            crack['y_end'],
            session  
        )
        crack_coordinates.append((crack['x_start'], crack['y_start'], crack['x_end'], crack['y_end']))

       
        # Insert crack details using raw SQLAlchemy
        crack_detail = CrackDetails(
            crack_name=crack['name'],
            crack_length=crack['length'],
            coordinates_id=coordinates_id,
            image_id=cracks_info['image_id'], 
            processing_date=datetime.now(timezone.utc), 
            crack_label=crack['name'] 
        )
        session.add(crack_detail)
    
    # Insert crack summary using raw SQL
    insert_crack_summary(
        image_id=cracks_info['image_id'], 
        crack_count=cracks_info['crack_count'], 
        session=session
    )

    session.commit()
    session.close()

    # Draw cracks on the in-memory image
    image_with_cracks = draw_cracks_on_image(cracks_info['preprocessed_image'])

    combined_image = combine_images(image, image_with_cracks)

   
    output_filename = f"combined_output_{image_file.filename}"

   
    output_path = os.path.join('outputs', output_filename)

  
    cv2.imwrite(output_path, combined_image)

 
    output_filename = f"output_{image_file.filename}"
    output_path = os.path.join('outputs', output_filename)
    cv2.imwrite(output_path, image_with_cracks)  

 
    return jsonify({
        'total_length': cracks_info['total_length'],
        'crack_count': cracks_info['crack_count'],
        'image_id': cracks_info['image_id'],
        'message': 'Crack details successfully inserted into the database',
        'output_image_path': output_path  # Path to the saved image file
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
