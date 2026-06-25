-- ============================================================
-- LMS DATABASE SCHEMA
-- Run this file in MySQL Workbench to set up the database
-- ============================================================

CREATE DATABASE IF NOT EXISTS lms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lms_db;

-- -------------------------------------------------------
-- USERS TABLE (All roles share this table)
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role ENUM('student', 'trainer', 'institute') NOT NULL,
    phone VARCHAR(20),
    profile_picture VARCHAR(255) DEFAULT 'default.png',
    is_active TINYINT(1) DEFAULT 1,
    approval_status ENUM('pending', 'approved', 'rejected') DEFAULT 'approved',
    approval_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- -------------------------------------------------------
-- INSTITUTES TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS institutes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    institute_name VARCHAR(200) NOT NULL,
    description TEXT,
    address TEXT,
    website VARCHAR(255),
    established_year YEAR,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- TRAINERS TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS trainers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    institute_id INT,
    specialization VARCHAR(200),
    experience_years INT DEFAULT 0,
    bio TEXT,
    qualification VARCHAR(200),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (institute_id) REFERENCES institutes(id) ON DELETE SET NULL
);

-- -------------------------------------------------------
-- STUDENTS TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    institute_id INT,
    date_of_birth DATE,
    gender ENUM('male','female','other'),
    address TEXT,
    education_level VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (institute_id) REFERENCES institutes(id) ON DELETE SET NULL
);

-- -------------------------------------------------------
-- CATEGORIES TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50) DEFAULT 'fa-book'
);

-- Insert default categories
INSERT INTO categories (name, description, icon) VALUES
('Programming', 'Software development and coding', 'fa-code'),
('Mathematics', 'Algebra, Calculus, Statistics', 'fa-calculator'),
('Science', 'Physics, Chemistry, Biology', 'fa-flask'),
('Language', 'English, Hindi, Regional languages', 'fa-language'),
('Business', 'Management, Finance, Marketing', 'fa-briefcase'),
('Design', 'Graphic Design, UI/UX', 'fa-palette'),
('Data Science', 'Machine Learning, AI, Analytics', 'fa-chart-bar'),
('Other', 'Miscellaneous subjects', 'fa-ellipsis-h');

-- -------------------------------------------------------
-- COURSES TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    thumbnail VARCHAR(255) DEFAULT 'course_default.png',
    trainer_id INT,
    institute_id INT,
    category_id INT,
    price DECIMAL(10,2) DEFAULT 0.00,
    duration_weeks INT DEFAULT 0,
    level ENUM('beginner','intermediate','advanced') DEFAULT 'beginner',
    status ENUM('draft','published','archived') DEFAULT 'draft',
    max_students INT DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trainer_id) REFERENCES trainers(id) ON DELETE SET NULL,
    FOREIGN KEY (institute_id) REFERENCES institutes(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- -------------------------------------------------------
-- LESSONS TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    video_url VARCHAR(500),
    file_attachment VARCHAR(255),
    lesson_order INT DEFAULT 1,
    duration_minutes INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- ENROLLMENTS TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active','completed','dropped') DEFAULT 'active',
    progress_percent INT DEFAULT 0,
    UNIQUE KEY unique_enrollment (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- ASSIGNMENTS TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_id INT NOT NULL,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATETIME,
    max_marks INT DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- SUBMISSIONS TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT NOT NULL,
    student_id INT NOT NULL,
    submission_text TEXT,
    file_path VARCHAR(255),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    marks_obtained INT,
    feedback TEXT,
    status ENUM('pending','graded') DEFAULT 'pending',
    FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- ANNOUNCEMENTS TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- NOTIFICATIONS TABLE
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    is_read TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- VERIFY ALL TABLES
-- -------------------------------------------------------
SHOW TABLES;
