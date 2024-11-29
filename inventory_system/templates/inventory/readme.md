
---

## **Template Files**

### **add_inventory.html**

- **Purpose**: Provides the form for adding new inventory items to the system.
- **Features**: 
  - Form for entering product details such as name, description, quantity, etc.
  - Accessible only to authorized users (Admins and Managers).

### **base.html**

- **Purpose**: The base template that provides a common layout for all other templates.
- **Features**:
  - Contains the header, footer, and navigation bar.
  - Other templates extend this base template to maintain a consistent look and feel across the application.

### **basichome.html**

- **Purpose**: The home page template, offering a basic view of the inventory system.
- **Features**: 
  - Display of a welcome message and basic navigation options.
  - Used as the default page after logging in.

### **delete_inventory.html**

- **Purpose**: Provides a confirmation page for deleting an inventory item.
- **Features**: 
  - Displays details of the item to be deleted.
  - Allows users to confirm the deletion.
  - Accessible only to Admins or Managers.

### **edit_inventory.html**

- **Purpose**: Provides the form for editing existing inventory items.
- **Features**:
  - Form pre-filled with current inventory data for editing.
  - Accessible to Admins and Managers.

### **edit_user.html**

- **Purpose**: Allows Admins to edit user details (e.g., roles, contact info).
- **Features**:
  - A form for updating user information.
  - Admin-only access.

### **home.html**

- **Purpose**: The main dashboard or home page for the user after logging in.
- **Features**:
  - Displays an overview of the inventory system.
  - Links to inventory management and user management functionalities.

### **inventory_list.html**

- **Purpose**: Displays a list of all inventory items.
- **Features**:
  - Table showing the details of inventory items.
  - Allows Admins and Managers to view and manage inventory items.
  - Option to delete or edit items.

### **login.html**

- **Purpose**: The login page template for user authentication.
- **Features**:
  - Form to enter username and password.
  - Redirects users to the appropriate dashboard based on their role (Admin, Manager, Staff).

### **permission_denied.html**

- **Purpose**: Displays when a user tries to access a page without the required permissions.
- **Features**:
  - Informative message explaining the lack of permissions.
  - Typically shown when users attempt to access restricted pages.

### **register.html**

- **Purpose**: The registration page template for new users.
- **Features**:
  - Form to create a new user account.
  - Admin users can create new accounts, assigning roles (Staff, Manager, Admin).

### **user_management.html**

- **Purpose**: Allows the Admin to manage system users.
- **Features**:
  - Display a list of users.
  - Ability to edit user roles and delete users.
  - Admin-only access.

---

## **Usage**

- The templates in this directory are designed to be rendered using Django’s template system.
- Templates are extended and used in the views via Django's `render()` method.
- The **base.html** template is extended by all other templates to provide consistent navigation and layout.
- **Authorization**: The access to certain templates is restricted based on the user's role (Admin, Manager, or Staff) through Django's built-in authentication and authorization mechanisms.

---

## **Customizing the Templates**

To customize any of the templates, you can:

1. Open the respective `.html` file in a code editor.
2. Modify the structure, content, or design according to your requirements.
3. Ensure that any dynamic data, such as inventory items, is passed from views to templates using Django’s context variables.

---

## **Contributing**

If you'd like to contribute to the design or functionality of the templates, feel free to open a pull request with your changes. We welcome contributions to enhance the usability and appearance of the **Shelvify Inventory Management System**.

---
