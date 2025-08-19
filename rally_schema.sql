-- Create database
CREATE DATABASE IF NOT EXISTS bootcamp_rally;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS bootcamp_rally.teams;
CREATE SCHEMA IF NOT EXISTS bootcamp_rally.cars;
CREATE SCHEMA IF NOT EXISTS bootcamp_rally.races;


-- TEAMS schema
CREATE OR REPLACE TABLE bootcamp_rally.teams.teams (
    team_id INTEGER AUTOINCREMENT PRIMARY KEY,
    team_name STRING NOT NULL UNIQUE,
    budget NUMBER(12,2) DEFAULT 10000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- CARS schema
CREATE OR REPLACE TABLE bootcamp_rally.cars.cars (
    car_id INTEGER AUTOINCREMENT PRIMARY KEY,
    team_id INTEGER REFERENCES bootcamp_rally.teams.teams(team_id),
    model STRING NOT NULL,
    speed NUMBER(5,0) NOT NULL,       
    horsepower NUMBER(5,0) NOT NULL,  
    handling NUMBER(3,0) NOT NULL,    
    durability NUMBER(3,0) NOT NULL,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RACES schema
CREATE OR REPLACE TABLE bootcamp_rally.races.races (
    race_id INTEGER AUTOINCREMENT PRIMARY KEY,
    race_name STRING NOT NULL,
    track_length_km NUMBER(6,2) DEFAULT 100,
    track_type STRING DEFAULT 'Gravel', -- Asphalt, Snow
    participation_fee NUMBER(10,2) DEFAULT 1000,
    prize_pool NUMBER(12,2) DEFAULT 5000,
    race_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE TABLE bootcamp_rally.races.race_results (
    result_id INTEGER AUTOINCREMENT PRIMARY KEY,
    race_id INTEGER REFERENCES bootcamp_rally.races.races(race_id),
    car_id INTEGER REFERENCES bootcamp_rally.cars.cars(car_id),
    team_id INTEGER REFERENCES bootcamp_rally.teams.teams(team_id),
    finish_time NUMBER(8,2), 
    position INTEGER,
    prize_awarded NUMBER(10,2) DEFAULT 0
);

-- Insert sample teams (team names and budget generated using AI)
INSERT INTO bootcamp_rally.teams.teams (team_name, budget) VALUES
('Red Bull Racing', 150000.00),
('Mercedes-AMG', 145000.00),
('Ferrari', 140000.00),
('McLaren', 120000.00),
('Alpine', 100000.00);

-- Insert sample cars (car characteristics generated using AI)
INSERT INTO bootcamp_rally.cars.cars (team_id, model, speed, horsepower, handling, durability) VALUES
(1, 'RB19', 350, 1050, 85, 90),
(1, 'RB18', 345, 1020, 80, 95),
(2, 'W14', 348, 1040, 85, 88),
(2, 'W13', 346, 1030, 80, 87),
(3, 'SF-23', 352, 1060, 80, 87),
(3, 'F1-75', 350, 1045, 85, 86),
(4, 'MCL60', 344, 1010, 75, 95),
(4, 'MCL36', 342, 1000, 75, 90),
(5, 'A523', 340, 980, 75, 92),
(5, 'A522', 338, 970, 70, 95);

-- Insert sample races (race characteristics generated using AI)
INSERT INTO bootcamp_rally.races.races (race_name, track_length_km, track_type, participation_fee, prize_pool) VALUES
('Monaco Grand Prix', 100, 'Asphalt', 1000.00, 10000.00),
('Swedish Rally', 120, 'Snow', 1500.00, 15000.00),
('Safari Rally Kenya', 110, 'Gravel', 1200.00, 12000.00);