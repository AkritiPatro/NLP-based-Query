CREATE DATABASE IF NOT EXISTS nlp_db;
USE nlp_db;

-- Drop tables if they exist
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS weather_reports;
DROP TABLE IF EXISTS vehicles;

-- Books Table
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    genre VARCHAR(100),
    publication_year INT
);

INSERT INTO books (title, author, genre, publication_year) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 1925),
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960),
('1984', 'George Orwell', 'Dystopian', 1949),
('The Catcher in the Rye', 'J.D. Salinger', 'Coming-of-Age', 1951),
('The Alchemist', 'Paulo Coelho', 'Philosophical', 1988);

-- Movies Table
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    director VARCHAR(255),
    release_year INT,
    rating DECIMAL(3,1)
);

INSERT INTO movies (title, director, release_year, rating) VALUES
('Inception', 'Christopher Nolan', 2010, 8.8),
('The Godfather', 'Francis Ford Coppola', 1972, 9.2),
('Titanic', 'James Cameron', 1997, 7.8),
('The Dark Knight', 'Christopher Nolan', 2008, 9.0),
('Parasite', 'Bong Joon-ho', 2019, 8.6);

-- Restaurants Table
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    cuisine VARCHAR(100),
    location VARCHAR(255),
    rating DECIMAL(3,1)
);

INSERT INTO restaurants (name, cuisine, location, rating) VALUES
('The Golden Spoon', 'Italian', 'New York', 4.5),
('Sushi Heaven', 'Japanese', 'Tokyo', 4.8),
('Spice Symphony', 'Indian', 'London', 4.3),
('BBQ Grill', 'American', 'Texas', 4.6),
('Café de Paris', 'French', 'Paris', 4.7);

-- Weather Reports Table
CREATE TABLE IF NOT EXISTS weather_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    temperature DECIMAL(5,2),
    humidity INT,
    conditions VARCHAR(100),
    report_date DATE
);

INSERT INTO weather_reports (city, temperature, humidity, conditions, report_date) VALUES
('New York', 22.5, 60, 'Sunny', '2025-03-01'),
('London', 18.3, 70, 'Cloudy', '2025-03-01'),
('Tokyo', 25.2, 55, 'Clear', '2025-03-01'),
('Paris', 20.0, 65, 'Rainy', '2025-03-01'),
('Sydney', 28.4, 50, 'Windy', '2025-03-01');

-- Vehicles Table
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(100),
    model VARCHAR(100),
    year INT,
    price DECIMAL(10,2)
);

INSERT INTO vehicles (make, model, year, price) VALUES
('Toyota', 'Corolla', 2022, 25000),
('Honda', 'Civic', 2021, 23000),
('Tesla', 'Model 3', 2023, 45000),
('Ford', 'Mustang', 2020, 55000),
('BMW', 'X5', 2022, 60000);

-- Check All Tables
SHOW TABLES;

-- Verify Data
SELECT * FROM books;
SELECT * FROM movies;
SELECT * FROM restaurants;
SELECT * FROM weather_reports;
SELECT * FROM vehicles;

