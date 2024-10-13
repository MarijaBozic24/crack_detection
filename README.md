# Crack Detection System

A Flask-based web application for detecting cracks in images, processing them using OpenCV, and storing the results in a PostgreSQL database.

## Features
- Upload an image for crack detection.
- Detect and display cracks overlaid on the original image.
- Store crack details (length, coordinates) and processing information (image ID, processing date) in the PostgreSQL database.
- Visualize preprocessed stages such as blurring, edge detection, etc.

## Setup

### Requirements
- Python 3.8+
- PostgreSQL
- Flask
- OpenCV
- SQLAlchemy

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/crack_detection.git
    cd crack_detection
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables in `.env`:
    ```bash
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    ```

4. Initialize the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

## Directory Structure
- `/app`: Contains the core Flask application code


## Image Processing
- Preprocessing: Image blurring, edge detection, and morphological transformations are applied to detect cracks.
- Stages of processing are saved under the `/static/outputs/` folder.

## Database
- Crack details and image metadata (such as processing date and image ID) are stored in PostgreSQL.


## License
This project is licensed under the MIT License.
