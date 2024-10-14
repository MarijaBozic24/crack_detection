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
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    DB_NAME=your_db_name
    ```

4. Run the application:
    ```bash
    python main.py
    ```
## Database Setup

To set up the PostgreSQL database for this project, follow the steps below:

### 1. Install PostgreSQL
Ensure that PostgreSQL is installed and running on your machine. If it's not installed, you can download it from the [official PostgreSQL website](https://www.postgresql.org/download/).

### 2. Create a Database
Once PostgreSQL is installed, create a new database that will be used for this project.

You can create the database by running the following commands in your PostgreSQL terminal:

```bash
psql -U postgres
```
Once inside the PostgreSQL shell, execute the command to create the database:
```sql
CREATE DATABASE your_database_name;
```
### 3. Set Up the Database Schema
The project comes with a schema.sql file that contains all necessary table definitions. To execute the SQL schema and set up your database:
1. Connect to the newly created database:
   ```bash
   psql -U postgres -d your_database_name
   ```
2. Run the SQL commands in schema.sql to set up your tables. You can use the following command to load the file:
   ```bash
   \i path/to/schema.sql
   ```
Replace path/to/schema.sql with the actual path to your schema.sql file.

## Directory Structure
- `/app`: Contains the core Flask application code


## Image Processing
- Preprocessing: Image blurring, edge detection, and morphological transformations are applied to detect cracks.

## Database
- Crack details and image metadata (such as processing date and image ID) are stored in PostgreSQL.


## License
This project is licensed under the MIT License.
