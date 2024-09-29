# Inventory-Management-API
Develop a backend API for an Inventory Management System that supports CRUD operations on inventory items, integrated with JWT-based authentication for secure access. It uses django rest API framework, MYSQL for the database, Redis for caching, and include unit tests to ensure functionality. 
# Inventory Management System API

## Overview

The Inventory Management System is a backend API developed using Django Rest Framework (DRF) that supports CRUD operations for managing inventory items. It utilizes PostgreSQL for data storage, Redis for caching frequently accessed items, and JWT-based authentication for secure access. This project includes comprehensive unit tests and a logging system for monitoring and debugging.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete inventory items.
- **JWT Authentication**: Secure all API endpoints with JSON Web Tokens.
- **Redis Caching**: Cache frequently accessed items for improved performance.
- **Logging**: Integrated logging system for tracking API usage and errors.
- **Unit Testing**: Comprehensive unit tests to ensure functionality and reliability.

## Technologies Used

- **Backend Framework**: Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Caching**: Redis
- **Authentication**: JSON Web Tokens (JWT)
- **Testing Framework**: Django's test framework

## Installation

### Prerequisites

- Python 3.x
- Django
- Django Rest Framework
- PostgreSQL
- Redis

### Clone the Repository

```bash
git clone https://github.com/vaddivijaya/Inventory-Management-API
Database Setup
Create a MYSQL database for the project.
Update the DATABASES setting in settings.py with your database credentials.
Redis Setup
Ensure Redis is installed and running on your local machine.

Migrate Database
Run the following command to apply migrations

python manage.py migrate
Create Superuser
Create a superuser to access the Django admin panel:

bash
Copy code
python manage.py createsuperuser
Run the Development Server
Start the Django development server:

bash
Copy code
python manage.py runserver
Access the API
The API will be available at http://127.0.0.1:8000/api/.

API Endpoints
Authentication

POST /api/token/: Obtain a JWT token.
POST /api/token/refresh/: Refresh the JWT token.
POST /register: User registration.
Inventory Items

POST /api/items/: Create a new inventory item.
GET /api/items/: Retrieve all inventory items.
GET /api/items/{item_id}/: Retrieve a specific inventory item.
PUT /api/items/{item_id}/: Update a specific inventory item.
DELETE /api/items/{item_id}/: Delete a specific inventory item.
Running Tests
Run the unit tests using the following command:

bash
Copy code
python manage.py test
Logging
The logging system is integrated to capture significant events and errors. Logs can be found in the configured logging directory.
