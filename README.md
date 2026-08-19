# VendorFlow

## 📌 Overview

VendorFlow is a web-based Vendor Management System designed to simplify and manage the interaction between vendors and suppliers.

The system provides a centralized platform where vendors can discover products, create requests for quotations, compare supplier quotations, and manage purchase orders. Suppliers can list and manage their products, respond to requests, and manage orders.

---

## 🚀 Features

### 👤 Vendor

- Vendor registration and login
- Vendor profile management
- Browse supplier products
- Search and view product details
- Create Requests for Quotation (RFQs)
- Receive supplier quotations
- Compare quotations
- Accept quotations
- Create and manage purchase orders
- Track order status
- View vendor dashboard and analytics

### 🏭 Supplier

- Supplier registration and login
- Supplier profile management
- Add products
- View listed products
- Edit products
- Delete products
- Manage product stock
- Receive vendor RFQs
- Submit quotations
- Manage purchase orders
- Update order/shipment status
- View supplier dashboard

### 📊 Dashboard & Analytics

- Vendor dashboard
- Supplier dashboard
- Purchase order tracking
- Product and inventory information
- Procurement-related statistics and graphs

### 🔐 Authentication

- User registration
- Secure login and logout
- Vendor and Supplier roles
- Role-based dashboard access
- Django authentication
- Admin panel for managing system data

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- Bootstrap
- Bootstrap Icons

### Backend

- Python
- Django
- Django REST Framework

### Database

- PostgreSQL

### Deployment

- Render

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 🏗️ Project Structure

```text
CodeSprout/
│
├── vendor/
│   ├── migrations/
│   ├── management/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── vendormanagement/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md