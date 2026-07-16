# Student Essential E-Commerce Website

> A complete Django-based E-Commerce platform designed specifically for students to purchase educational products such as books, stationery, calculators, accessories, and study materials. The application provides secure authentication, role-based access control, shopping cart functionality, coupon discounts, multiple payment options, order management, and an admin dashboard.

---

# 📌 Project Overview

Student Essential E-Commerce Website is a web application developed using **Python Django** following the **Model-View-Template (MVT)** architecture.

The platform allows students to browse educational products, add them to the cart, apply discount coupons, choose a payment method, and place orders easily.

Administrators can manage products, users, orders, pending admin requests, and view sales reports through a dedicated dashboard.

---

# 🚀 Features

## 👤 User Features

* User Registration
* Secure Login & Logout
* Role-Based Authentication
* Browse Products
* Product Categories
* Product Details
* Add to Cart
* Increase / Decrease Quantity
* Remove Cart Items
* Coupon Discount System
* Checkout
* QR Payment
* Cash on Delivery (COD)
* Card Payment
* Order Placement
* Order History
* Responsive User Interface

---

## 👨‍💼 Admin Features

* Admin Login
* Admin Approval System
* Dashboard
* Add Products
* Edit Products
* Delete Products
* Manage Users
* Approve/Reject Admin Requests
* Manage Orders
* Update Order Status
* Sales Report
* Download Sales Report (CSV)

---

# 🛠 Tech Stack

## Frontend

* HTML5
* CSS3
* JavaScript

## Backend

* Python
* Django

## Database

* SQLite

## Tools

* Visual Studio Code
* Git
* GitHub

---

# 📂 Project Structure

```text
Student-Essential-Ecommerce/
│
├── media/
│
├── static/
│
│── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── cart.html
│   ├── checkout.html
│   ├── admin_dashboard.html
│   ├── manage_products.html
│   ├── orders.html
│   ├── users.html
│   └── ...
│
├── app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── ...
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/student-essential-ecommerce.git
```

Move into project folder

```bash
cd student-essential-ecommerce
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

Start Development Server

```bash
python manage.py runserver
```

Open Browser

```
http://127.0.0.1:8000/
```

---

# 🔐 Authentication Flow

```
User
      │
      ▼
Registration
      │
      ▼
Login
      │
      ▼
Authentication
      │
      ▼
Role Verification
      │
 ┌────┴────┐
 ▼         ▼
User     Admin
 │          │
 ▼          ▼
Home     Dashboard
```

---

# 🛒 Shopping Flow

```
Home

↓

Browse Products

↓

Product Details

↓

Add To Cart

↓

Cart

↓

Coupon Apply

↓

Checkout

↓

Payment

↓

Order Success

↓

My Orders
```

---

# 👨‍💼 Admin Workflow

```
Admin Login

↓

Dashboard

↓

Manage Products

↓

Manage Users

↓

Approve Requests

↓

Manage Orders

↓

Sales Report

↓

Download Report
```

---

# 🗄 Database Tables

### User

* id
* username
* email
* password

---

### UserProfile

* user
* role
* approved

---

### Product

* id
* name
* description
* price
* image
* category

---

### Cart

* id
* user
* product
* quantity

---

### Order

* id
* user
* product
* quantity
* total_price
* payment_method
* status
* created_at

---

### Coupon

* id
* code
* discount
* active

---

# 🎯 Main Modules

## User Module

* Registration
* Login
* Home Page
* Category View
* Product Details
* Cart
* Coupon
* Checkout
* Payment
* Order

---

## Admin Module

* Dashboard
* Products
* Users
* Orders
* Pending Requests
* Reports

---

# 💳 Payment Methods

* Cash on Delivery (COD)
* QR Payment (UPI)
* Card Payment

---

# 🎟 Coupon System

* Active Coupon Validation
* Percentage Discount
* Final Amount Calculation
* Session-Based Discount

---

# 📊 Sales Report

The application provides

* Total Orders
* Total Revenue
* Download CSV Report

---

# 🔒 Security Features

* Django Authentication
* Password Hashing
* Role-Based Access Control
* Login Required Decorator
* Admin Approval System
* Session Management

---

# 📈 Future Enhancements

* Razorpay Payment Gateway
* Stripe Integration
* Email Notifications
* OTP Verification
* Product Reviews
* Wishlist
* Product Search
* AI Product Recommendation
* Inventory Management
* Order Tracking
* Mobile Application
* REST API
* PostgreSQL/MySQL Support

---

# 📸 Screenshots

### User Module

* Login Page
* Register Page
* Home Page
* Categories
* Product Details
* Cart
* Checkout
* Payment
* My Orders

### Admin Module

* Dashboard
* Manage Products
* Manage Users
* Orders
* Pending Requests
* Sales Report

---

# 📚 Technologies Used

| Technology | Purpose             |
| ---------- | ------------------- |
| Python     | Backend Programming |
| Django     | Web Framework       |
| HTML       | Structure           |
| CSS        | Styling             |
| JavaScript | Interactivity       |
| SQLite     | Database            |
| Git        | Version Control     |
| GitHub     | Source Code Hosting |

---

# 👨‍💻 Developed By

# 👥 Team Members

This project was developed as a collaborative academic project by the following team members:

| Name | Role |
|------|------|
| Ankit Prashar | Backend Developer, Database Design, Authentication, Admin Panel, Project Documentation |
| Ritu Rani | Frontend Development, UI Design, HTML & CSS |
| Anjali Kumari | Testing, Documentation, Module Design |
| Bhavna Chandan | Requirement Analysis, Testing, Report Preparation |


Bachelor of Computer Applications (BCA)

L.N. Mishra College of Business Management

Muzaffarpur, Bihar

GitHub: **[https://github.com/Ankitprashar04](https://github.com/Ankitprashar04)**

LinkedIn: **[https://linkedin.com/in/ankit-prashar-052213300](https://linkedin.com/in/ankit-prashar-052213300)**

---

# 📄 License

This project is developed for **educational and academic purposes** as part of the Bachelor of Computer Applications (BCA) final year project.

---

# ⭐ If you like this project

Please consider giving it a **⭐ Star** on GitHub to support the project and encourage future development.
