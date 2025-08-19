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