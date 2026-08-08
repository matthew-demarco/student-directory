# Student Directory

A full-stack web application built with Flask and PostgreSQL that allows users to add, view, edit, and delete students.

## Features

- Add new students
- View all students stored in PostgreSQL
- Edit existing student information
- Delete students
- Server-side input validation
- Flash messages for invalid input
- 404 handling for students that do not exist
- PostgreSQL database persistence
- Environment variables for database credentials and secrets

## Tech Stack

- Python
- Flask
- PostgreSQL
- psycopg
- HTML
- Jinja
- python-dotenv
- Git

## How It Works

The browser sends an HTTP request to the Flask application.

Flask processes the request and communicates with PostgreSQL when database access is required.

    Browser
       ↓
    Flask
       ↓
    PostgreSQL
       ↓
    Flask
       ↓
    HTML Response
       ↓
    Browser

## CRUD Operations

The application supports all four CRUD operations:

| Operation | Description |
| --- | --- |
| Create | Add a new student |
| Read | View students stored in PostgreSQL |
| Update | Edit an existing student |
| Delete | Remove a student |

## Routes

### Home

    GET /

Displays all students stored in the database.

### Add Student

    POST /add

Receives a student's name and school from the form and inserts a new row into PostgreSQL.

### Edit Student

    GET /edit/<student_id>

Retrieves one student from PostgreSQL and displays their current information in an edit form.

### Update Student

    POST /update/<student_id>

Updates an existing student's name and school.

### Delete Student

    POST /delete/<student_id>

Deletes the selected student from PostgreSQL.

## Project Structure

    student-directory/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── .gitignore
    ├── .env
    └── templates/
        ├── home.html
        └── edit.html

The `.env` file is ignored by Git and should not be uploaded to GitHub.

## Environment Variables

Create a `.env` file in the root of the project:

    DB_NAME=practice
    DB_USER=student_app
    DB_PASSWORD=your_database_password
    DB_HOST=localhost
    SECRET_KEY=your_secret_key

Do not commit the `.env` file to GitHub.

## Installation

### 1. Clone the repository

    git clone <repository-url>
    cd student-directory

### 2. Create a virtual environment

    python3 -m venv venv

### 3. Activate the virtual environment

    source venv/bin/activate

### 4. Install dependencies

    pip install -r requirements.txt

### 5. Configure PostgreSQL

Create a PostgreSQL database and a `students` table.

Example:

    CREATE TABLE students (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        school TEXT NOT NULL
    );

Then add your PostgreSQL credentials to the `.env` file.

### 6. Run the application

    python3 app.py

Open the application in your browser at:

    http://127.0.0.1:5000

## Validation

The application performs server-side validation before inserting or updating student records.

Input is cleaned using `.strip()` so whitespace-only values are rejected.

If the name or school is empty, Flask displays an error message instead of modifying the database.

## Security

Database credentials and the Flask secret key are stored in environment variables instead of being hardcoded in the application.

The `.env` file is excluded from Git using `.gitignore`.

## What I Learned

Building this project helped me understand:

- How Flask routes handle HTTP requests
- How GET and POST requests work
- How HTML forms communicate with a backend
- How Flask communicates with PostgreSQL
- How SQL SELECT, INSERT, UPDATE, and DELETE operations work
- How database transactions use commit()
- How Jinja templates display dynamic data
- How redirects work after POST requests
- How to implement server-side validation
- How Flask flash messages and sessions work
- How to handle missing database records
- How environment variables separate secrets from source code
- How Git tracks the development of an application

## Future Improvements

- Improve the interface with CSS
- Add search and filtering
- Add user authentication
- Add automated tests
- Build JSON REST API endpoints
- Dockerize the application
- Deploy the application online

## Author

Matthew DeMarco  
Computer Science Student at Florida State University
