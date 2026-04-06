 🖥️ My Web Development Projects

This repository contains multiple web development projects created using **HTML, CSS, JavaScript, Flask, and MySQL**. Each project demonstrates different skills in frontend and full-stack development.

1️⃣ Dancing Robot

Description:
An interactive frontend project where a robot dances using CSS animations and JavaScript.

Features:

* Head, arms, and leg animations
* Smooth dance movements
* Fully frontend-based, no backend required

Technologies:
HTML, CSS, JavaScript

Setup / Run:

1. Open the project folder.
2. Open `index.html` in a web browser.

2️⃣ Calculator

Description:
A simple web-based calculator capable of performing basic arithmetic operations.

Features:

* Addition, subtraction, multiplication, division
* Handles decimal operations
* Interactive and responsive layout

Technologies:
HTML, CSS, JavaScript

Setup / Run:

1. Open the project folder.
2. Open `calculator.html` in a web browser.

3️⃣ Frontend Web Development Projects

Description:
Various mini-projects showcasing HTML and CSS skills, including landing pages, styled forms, and interactive UI elements.

Features:

* Responsive design
* Styled forms, buttons, and interactive elements
* Easy to customize for different layouts

Technologies:
HTML, CSS

Setup / Run:

1. Open any project folder.
2. Open `index.html` in a web browser.

4️⃣ Flash & HTML

Description:
A Flask-based web project that handles user input through forms, validates input, and shows flash messages for success or error.

Features:

* Collect user input through web forms
* Display flash messages for validation
* Redirect to result page after submission

Technologies:
Python, Flask, HTML, CSS

Setup / Run:

1. Install Flask:

```bash
pip install flask
```

2. Run the Flask app:

```bash
python app.py
```

3. Open `http://127.0.0.1:5000/` in a web browser.

5️⃣ Student Details Entry System (Flask + MySQL)

Description:
A full-stack student management system that stores and displays student records in a MySQL database.

Features:

* Add student records with: name, age, gender, email, phone, department, GPA, and admission date
* View all student records in a table
* Validation for numeric and required fields

Technologies:
Python, Flask, MySQL, HTML, CSS

Setup / Run:

1. Install required dependencies:

```bash
pip install flask mysql-connector-python
```

2. Create MySQL database and table:

```sql
CREATE DATABASE studentdb;

USE studentdb;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    gender ENUM('Male','Female','Other'),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(10),
    department VARCHAR(50),
    gpa DECIMAL(3,2),
    admission_date DATE DEFAULT (CURRENT_DATE)
);
```

3. Run the Flask app:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000/` to use the application.


⚡ Notes

* Make sure **MySQL server is running** before using the Student Details project.
* Python 3.x is required for Flask projects.
* All frontend-only projects can run directly in a browser without a server.

6️⃣ Study Group Finder (Flask + SQLite/MySQL)

Description:
A full-stack web application that helps students create, join, and chat in study groups online.

Features:

Register and login as a user
Create new study groups with name and description
Join existing study groups
Chat with members of a group in real-time
View all available study groups

Technologies:
Python, Flask, SQLite (or MySQL), HTML, CSS, JavaScript

Setup / Run:

Install required dependencies:
pip install flask flask_sqlalchemy flask_login
Initialize the database (SQLite example):
from app import app
from models import db

with app.app_context():
    db.create_all()

⚠️ If using MySQL, update config.py with your MySQL connection string and create tables accordingly.

Run the Flask app:
python app.py
Open in your browser:
http://127.0.0.1:5000/

⚡ Notes:

Python 3.x is required
Keep CSS and JS in the static/ folder
HTML templates must be in the templates/ folder
SQLite is default; can switch to MySQL if needed

