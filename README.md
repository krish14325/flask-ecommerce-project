# Flask E-Commerce Project

A full-stack E-Commerce web application built using **Python, Flask, HTML, CSS, and MySQL**. This project allows users to register, log in, browse products, search products, manage their cart, place orders, and view their order history.

## Features

### User Authentication

* User Registration
* User Login
* Session Management
* Logout Functionality
* Form Validation

### Product Management

* View All Products
* Product Details Page
* Product Search
* Category-Based Filtering
* Product Images

### Shopping Cart

* Add Products to Cart
* Remove Products from Cart
* Increase Quantity
* Decrease Quantity
* Automatic Stock Management
* Product-Wise Total Calculation
* Grand Total Calculation

### Order Management

* Place Orders
* Store Order Details
* Store Ordered Products
* View Order History
* View Ordered Product Details

### Database Features

* Users Table
* Products Table
* Cart Table
* Orders Table
* Order Items Table
* Category Management

## Technologies Used

### Backend

* Python
* Flask

### Frontend

* HTML5
* CSS3

### Database

* MySQL

### Tools

* VS Code
* MySQL Workbench
* Git
* GitHub

## Database Schema

### USERS

Stores user account information.

### PRODUCTS

Stores product details, stock, category, and image information.

### CART

Stores products currently added to a user's cart.

### ORDERS

Stores order information and total amount.

### ORDER_ITEMS

Stores products associated with each order.

## Project Structure

electronics_store/

├── static/

│ ├── images/

│ └── style.css

├── templates/

│ ├── login.html

│ ├── register.html

│ ├── dashboard.html

│ ├── product.html

│ ├── cart.html

│ ├── orders.html

│ ├── viewdetails.html

│ ├── search.html

│ └── category.html

├── app.py

└── README.md

## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/flask-ecommerce-project.git
```

2. Navigate to project directory

```bash
cd flask-ecommerce-project
```

3. Install dependencies

```bash
pip install flask mysql-connector-python
```

4. Create MySQL database and required tables.

5. Update database credentials in app.py.

6. Run the application

```bash
python app.py
```

7. Open browser

```text
http://127.0.0.1:5000
```

## Future Improvements

* Admin Panel
* Product Management Dashboard
* Order Tracking
* Payment Gateway Integration
* User Profile Management
* Product Reviews and Ratings
* Responsive UI Design
* Password Hashing
* Email Verification
* REST API Development

## Learning Outcomes

This project helped me learn:

* Flask Routing
* Jinja Templates
* Session Management
* CRUD Operations
* SQL Joins
* Database Design
* Form Handling
* Search Functionality
* Cart Management Logic
* Order Processing Logic
* Git & GitHub Workflow

## Author

Krishna Gupta

Built as a learning project to gain practical experience in Full Stack Web Development using Flask and MySQL.
