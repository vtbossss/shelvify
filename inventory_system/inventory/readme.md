# **Inventory App - Shelvify**

The **Inventory app** in **Shelvify** manages all inventory-related operations, including adding, editing, viewing, and deleting inventory items. This app also handles user permissions and role-based access control (RBAC) for inventory management.

---


## **Core Files**

### **`__init__.py`**

- **Purpose**: Marks this directory as a Python package.
- **Location**: Found in the root of the `inventory` directory and the `migrations` folder.

### **`admin.py`**

- **Purpose**: Configures the admin interface for managing inventory items in the Django admin panel.
- **Features**:
  - Registers models like `Product` with Django's admin site.
  - Allows admins to manage inventory through a user-friendly interface.

### **`apps.py`**

- **Purpose**: Configures the app for Django's app registry.
- **Features**:
  - Defines the app configuration class `InventoryConfig`, which registers the app with Django.

### **`forms.py`**

- **Purpose**: Defines the forms used for creating and updating inventory items.
- **Features**:
  - Includes Django `ModelForm` classes for creating and editing product information.
  - Ensures that inventory-related data is validated before being saved to the database.

### **`middleware.py`**

- **Purpose**: Contains middleware for handling custom request processing.
- **Features**:
  - Includes functionality for logging, session management, or custom user authentication/authorization checks for inventory-related routes.

### **`models.py`**

- **Purpose**: Contains the database models for the application.
- **Key Models**:
  - **`Product`**: Represents a product in the inventory, including fields like name, quantity, and price.
  - **`Inventory`**: A model that handles the inventory records and links to the `Product` model.

### **`permissions.py`**

- **Purpose**: Contains custom permission classes to enforce role-based access control (RBAC) in the inventory app.
- **Features**:
  - Permissions ensure that only users with the right roles (Admin, Manager, etc.) can perform certain actions like adding, updating, or deleting inventory items.

### **`serializers.py`**

- **Purpose**: Contains serializers to convert complex data types (like `Product` objects) into Python data structures (JSON).
- **Features**:
  - Converts models to JSON for API endpoints.
  - Handles validation of incoming data when interacting with inventory through API requests.

### **`tests.py`**

- **Purpose**: Contains the test cases for ensuring the correctness of the inventory app’s functionality.
- **Features**:
  - Includes unit tests for inventory actions such as adding, deleting, or updating products.
  - Ensures role-based permissions are correctly applied.
  - Tests inventory-related API endpoints.

### **`urls.py`**

- **Purpose**: Defines the URL routing for the inventory-related views and API endpoints.
- **Features**:
  - Maps URL patterns to views like `add_inventory`, `edit_inventory`, and `inventory_list`.
  - Includes API routes for CRUD operations on inventory items.

### **`views.py`**

- **Purpose**: Contains the logic for handling inventory-related HTTP requests.
- **Features**:
  - Handles user requests to add, edit, view, and delete inventory items.
  - Includes views that render HTML templates as well as API views for RESTful interactions.

---

## **Migrations Directory**

### **`migrations/`**

- **Purpose**: Contains database migration files that Django generates for tracking changes in the database schema.
- **Files**:
  - **`0001_initial.py`**: The initial migration for creating the `Product` and `Inventory` models in the database.
  - **`0002_alter_user_managers.py`**: A migration for altering user managers as part of the user model setup.

---

## **Pycache Directory**

### **`__pycache__/`**

- **Purpose**: Contains compiled Python files (.pyc), which are generated automatically when Python code is executed. These files speed up loading and execution but can generally be ignored in version control (usually excluded via `.gitignore`).

---

## **Usage**

- The `inventory` app handles everything related to inventory management, including models for products, permissions, forms for managing inventory data, and views for user interaction.
- **Admin Role**: Can add, edit, and delete inventory items.
- **Manager Role**: Can edit and update inventory but cannot delete items.
- **Staff Role**: Can view inventory data but cannot make any changes.

---

## **Contributing**

Contributions are welcome! If you'd like to contribute to the inventory management features, add new models, or fix bugs, feel free to open an issue or a pull request in the [GitHub repository](https://github.com/your-username/shelvify/issues).

---

## **License**

This project is open-source and licensed under the [MIT License](LICENSE).
