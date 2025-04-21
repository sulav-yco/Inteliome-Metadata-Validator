-- Departments Table (with unique department_code)
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_code VARCHAR(10) UNIQUE,  -- NEW unique column
    name VARCHAR(100) NOT NULL
);

-- Professors Table (foreign key now references department_code)
CREATE TABLE professors (
    professor_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_codee VARCHAR(10),  -- FK now refers to a unique column
    FOREIGN KEY (department_codee) REFERENCES departments(department_code)
);

-- Students Table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    enrollment_year INT
);

-- Courses Table
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    department_id INT,
    professor_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
);

-- Enrollments Table
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
