# CST Hostel Management System

A web-based application built with Django for managing hostel accommodations, including room assignments, student information, and a review system.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Security](#security)
- [Scalability](#Scalability)
- [Code_quality](#Code_quality)
- [Testing](#testing)

## Features

- User authentication and authorization
- Hostel room assignments
- Student information management
- Review system with ratings (0 to 5 stars)
- Admin dashboard for managing hostels and users booking schedule
- User can get help from the counselor through the help page
- Consist of menu where the user can know the menu served in the College of Science Technology hostel

## Requirements

- Python 3.x
- Django 3.x or later
- SQLite (default) or other database systems (PostgreSQL, MySQL, etc.)
- Django-filter 
- Pillow
- selenium(For end-to-end testing)

## Installation

# Create a virtual environment

- python -m venv Yourenivronment

# Activate the virtual environment
- myenv\Scripts\activate

# Download the neccessary requirements from requirement.txt
- pip install -r requirements.txt

# Move to the project directory
- cd myproject_name

# Apply the migration
- py manage.py migrate

# Run the project 
- py manage.py runserver

## Usage

- Can be used in the hostel management system for the college

## Security

# Django provides several built-in security features that help protect your database

- SQL Injection Protection: Django’s ORM automatically escapes query parameters to prevent SQL injection attacks.

- Cross-Site Request Forgery (CSRF) Protection: Django includes middleware to protect against CSRF attacks.

- XSS Protection: Django templates auto-escape variables to prevent cross-site scripting (XSS) attacks.

## Scalability

 # ORM Efficiency
 - Optimize your Django ORM queries by using select_related, prefetch_related, and avoiding N+1 query problems.

## Code_quality

# showing the code where the main.html is used frequently

## Testing

-  Unit test done in the tests.py where the each model is test with the random data 
-  Integration tests done on for the Booking Room View
-  End-to-End testing done in the test case 

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Dendup1234/hms_cst.git
   cd hms_cst
