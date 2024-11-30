
# **Shelvify - Inventory Management System**

**Shelvify** is a comprehensive, secure, and user-friendly **Inventory Management System (IMS)** designed to help businesses efficiently track, manage, and secure their inventory. It leverages **Role-Based Access Control (RBAC)**, **JWT Authentication**, and secure front-end and back-end authorization to ensure only authorized users interact with the system.

---

## **Key Features**

### **Role-Based Access Control (RBAC)**

- **Admin**: Full control over inventory, user roles, and system configurations.
- **Manager**: Can update inventory quantities and product details.
- **Staff**: Read-only access to view inventory details.

### **Secure Authentication**

- **JWT Authentication**: Secure API endpoints and protect user data.

### **Dual-Layer Security**

- **Authorization Verification** on both **front-end** and **back-end** to prevent unauthorized access.

### **Password Validation**

- Enforces strong passwords with custom validation rules to enhance security.

### **Rate Limiting & Lockout**

- Integrated with the **AXES package** to limit login attempts and lock users out after multiple failed attempts, preventing brute-force attacks.

### **Containerization with Docker**

- **Dockerized application** ensures consistent environments for development, testing, and deployment.

### **SSL/TLS Encryption (HTTPS)**

- Hosted on **PythonAnywhere**, ensuring secure communication between client and server via **HTTPS**.

---

## **Demo**

Explore the live demo of **Shelvify** hosted on **PythonAnywhere**:

https://shelvify.pythonanywhere.com

### **Test Credentials:**

- **Username**: `admin`
- **Password**: `12345678`

> **Note**: By default, all new users are assigned the **Staff** role. Only the **Admin** can upgrade roles to **Manager** or **Admin**.

---

## **Installation Guide**

Follow these simple steps to set up **Shelvify** locally:

### **Prerequisites**

Before you begin, make sure you have the following installed on your system:

- **Python 3.13+**  
- **Docker** (optional, for containerized environment)

### **Clone the Repository**

To get started, clone the repository and navigate into the project folder:

```bash
git clone https://github.com/your-username/shelvify.git
cd shelvify
```

Then, navigate into the **`inventory_system`** directory:

```bash
cd inventory_system
```

### **Create the `.env` File**

Create a `.env` file to store your Django settings, such as the `SECRET_KEY` and `DEBUG` variables. Run the following command to create the file:

```bash
touch .env
```

Next, open the `.env` file and add the following environment variables:

```env
DJANGO_SECRET_KEY=your-secret-key  # Replace with a strong secret key
DEBUG=True  # Set to False in production
```

You can generate a secure `SECRET_KEY` by running this Python snippet(Note: u must have django installed in order to get the secretkey):

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### **Build and Start the Application Using Docker**

1. **Build Docker Containers:**

   Run the following command to build the Docker containers:

   ```bash
   docker-compose build
   ```

2. **Start the Application:**

   Run the following command to start the application:

   ```bash
   docker-compose up
   ```

After running the commands, the application will be running and accessible at `http://localhost:8000`.

## **Screentshots**

**Admin dashboard**


![Admin dashboard](https://github.com/user-attachments/assets/57d9b30b-87a7-4b6b-abc4-d94cf2249d30)


**Admin inventory page**


![Admin inventory page](https://github.com/user-attachments/assets/e20ce0a6-cda6-42fc-8483-78b0bd45bdab)


**Admin User management page**


![Admin User management page](https://github.com/user-attachments/assets/c2673b20-d7b7-497b-af40-5450216ff41c)


**User dashboard**


![User dashboard](https://github.com/user-attachments/assets/c16c6f6b-365e-48da-b1e5-ab4623a94ccf)


**User inventory page**


![User inventory page](https://github.com/user-attachments/assets/530cec8a-4a33-4a08-a045-3dc11c7fbb00)


**Manager Dashboard**


![Manager Dashboard](https://github.com/user-attachments/assets/14ff3838-b80b-4e94-aa33-460fb75dd48b)


**Manager Inventory Page**


![Manager Inventory Page](https://github.com/user-attachments/assets/bd5b6216-20aa-4e02-a7f3-b526c7883c54)


## **Troubleshooting**

If you encounter any issues, consider checking the following:

1. **Missing `.env` File**: Ensure the `.env` file exists and contains the correct `DJANGO_SECRET_KEY` and `DEBUG` variables.
2. **Docker Not Installed**: Ensure Docker is installed and running if you're using the containerized environment.

For any other issues, feel free to open an issue on the [GitHub repository](https://github.com/vtbossss/shelvify/issues).

---


