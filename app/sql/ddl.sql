-- Create departments table
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    department VARCHAR(255)
);

-- Create jobs table
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    job VARCHAR(255)
);

-- Create employees table with foreign keys
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    datetime TIMESTAMP,
    department_id INT,
    job_id INT
);
