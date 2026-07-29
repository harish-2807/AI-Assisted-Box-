# AI-Assisted Box Selection System

A Django and Django REST Framework-based backend system that recommends the most suitable shipping box for an ecommerce order.

The system considers product dimensions, product weight, box internal dimensions, maximum weight capacity, and box cost to determine which available box can safely accommodate an order.

## GitHub Repository

[Add your GitHub repository link here]

## Project Overview

In an ecommerce warehouse, when a customer places an order, the warehouse team needs to select an appropriate shipping box.

Each product has:

- Length
- Width
- Height
- Weight

Each shipping box has:

- Internal length
- Internal width
- Internal height
- Maximum weight capacity
- Cost

This project provides a backend system that evaluates an order and recommends the most suitable available box.

## Features

- Product management
- Shipping box management
- Order management
- Multiple products per order
- Product quantity handling
- Product and box dimension validation
- Total order weight calculation
- Total product volume calculation
- Product rotation/orientation handling
- 3D packing validation
- Box recommendation based on defined selection criteria
- REST API using Django REST Framework
- Automated testing

## Technology Stack

- Python
- Django
- Django REST Framework
- SQLite
- Django ORM
- Git
- GitHub

## Project Structure

```text
ecommerce-warehouse/
│
├── box_selection/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
├── README.md
├── AI_USAGE.md
├── AI_CHAT_TRANSCRIPT.md
└── TEST_OUTPUT.md