# **Inventory System - Shelvify**

This directory contains the core functionality and settings of the **Shelvify Inventory Management System**. It includes the main project configuration files, Django settings, and essential components for the application to run.

---

## **Core Files**

### **`__init__.py`**

- **Purpose**: This file indicates that the directory should be treated as a Python package.
- **Location**: Found in both the root of the `inventory_system` directory and the `migrations` folder.

### **`asgi.py`**

- **Purpose**: Configures the ASGI application for the project. This file is used for asynchronous communication in Django (typically for WebSockets or real-time features).
- **Features**:
  - It sets up the ASGI application to handle incoming connections.
  - Used when deploying the project with an ASGI server like Daphne or Uvicorn.

### **`settings.py`**

- **Purpose**: Contains the main settings for the project, including configurations for the database, installed apps, middleware, security settings, and other Django configurations.
- **Key Sections**:
  - **Database Configuration**: Settings for connecting to the database (SQLite by default).
  - **Installed Apps**: Includes Django apps like `django.contrib.admin`, `inventory`, and others.
  - **Middleware**: Defines the middleware stack used in the application for request/response handling.
  - **Static Files and Media**: Directories and settings for serving static assets (CSS, JS) and media files.
  - **Authentication**: Configurations for user authentication, including login and session management.
  - **Security**: Settings like `SECRET_KEY`, `DEBUG`, and other security measures.

### **`urls.py`**

- **Purpose**: Defines the URL routing for the Django project.
- **Features**:
  - Maps URL patterns to views in the application.
  - Includes routes for the inventory system, user authentication, and admin panel.
  - URL patterns are linked to respective views in the `inventory` app.

### **`wsgi.py`**

- **Purpose**: Configures the WSGI application for the project, enabling it to communicate with web servers for serving the application.
- **Features**:
  - This file is used when deploying the project with a WSGI server like Gunicorn or uWSGI.

---

## **Migrations Directory**

### **`migrations/`**

- **Purpose**: Contains database migration files that Django generates for tracking changes in the database schema.
- **Files**:
  - **`0001_initial.py`**: The initial migration when the database schema is first created.
  - **`0002_alter_user_managers.py`**: A migration for altering the user managers as part of the user model setup.

---

## **Pycache Directory**

### **`__pycache__/`**

- **Purpose**: This directory contains compiled Python files (.pyc), which are generated automatically when Python code is executed. These files speed up loading and execution but can generally be ignored in version control (usually excluded via `.gitignore`).

---

## **Usage**

- The files in this directory are essential for the operation of the **Shelvify Inventory Management System**.
- **Settings File**: `settings.py` must be configured for different environments (development, production). This includes database connection, security settings, and installed apps.
- **URL Routing**: Modify `urls.py` to add or modify routes as the project grows.
- **Database Migrations**: Run migrations to apply changes to the database schema using Django's migration system.

---

## **Contributing**

Contributions are welcome! If you'd like to contribute to the core functionality or make improvements to the project, feel free to open a pull request or an issue on the GitHub repository.

---

