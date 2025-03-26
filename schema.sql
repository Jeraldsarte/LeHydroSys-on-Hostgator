CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    air_temp FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    water_temp FLOAT NOT NULL,
    water_level FLOAT NOT NULL,
    ph FLOAT NOT NULL,
    tds FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
