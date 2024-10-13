CREATE TABLE crackcoordinates (
    id SERIAL PRIMARY KEY,
    x_start INT,
    y_start INT,
    x_end INT,
    y_end INT
);

CREATE TABLE crackdetails (
    id SERIAL PRIMARY KEY,
    crack_name VARCHAR(255),
    crack_length FLOAT,
    coordinates_id INT REFERENCES crackcoordinates(id)
);

CREATE TABLE cracksummary (
    image_id UUID PRIMARY KEY,
    crack_count INT
);

ALTER TABLE crackdetails
ADD COLUMN image_id VARCHAR(36) NOT NULL,
ADD COLUMN processing_date TIMESTAMP DEFAULT NOW() NOT NULL,
ADD COLUMN crack_label VARCHAR(255);

