# AI-Assisted Box Selection System

A Django and Django REST Framework-based system that recommends the most suitable shipping box for an ecommerce order based on product dimensions, product weight, box dimensions, maximum weight capacity, and box cost.



## Project Overview

In an ecommerce warehouse, selecting the correct shipping box for an order is important for reducing unused space, packaging costs, and operational effort.

This project provides a backend system that:

- Stores product information and dimensions.
- Stores available shipping boxes and their capacities.
- Creates orders containing multiple products and quantities.
- Calculates the total weight and volume of an order.
- Checks whether products can physically fit inside available boxes.
- Considers different product orientations.
- Recommends the smallest feasible box according to the defined selection criteria.
- Provides REST APIs for managing products, boxes, and orders.
- Provides a box recommendation API for an order.

## Key Features

### Product Management

Each product contains:

- Product name
- Length
- Width
- Height
- Weight

### Box Management

Each shipping box contains:

- Box name
- Internal length
- Internal width
- Internal height
- Maximum weight capacity
- Cost

### Order Management

An order can contain:

- Multiple products
- Product quantities
- Order status
- Order creation timestamp

### Box Recommendation

The recommendation system considers:

1. Total order weight.
2. Box maximum weight capacity.
3. Total product volume.
4. Box internal volume.
5. Individual product dimensions.
6. Product orientation and rotation.
7. Multiple products and quantities.
8. Physical 3D packing constraints.

The system selects the smallest feasible box based on internal volume.

If multiple feasible boxes have the same internal volume, the cheaper box is preferred.

If no suitable box can accommodate the order, the system returns a clear no-suitable-box result.

## Selection Criteria

The recommended box is selected using the following order:

1. The box must support the total weight of the order.
2. All products must physically fit inside the box.
3. Product quantities must be considered.
4. Product rotations are considered using 90-degree orthogonal orientations.
5. The smallest feasible box by internal volume is preferred.
6. If box volumes are equal, the lower-cost box is preferred.
7. If volume and cost are equal, maximum weight capacity and box ID are used as deterministic tie-breakers.

## Technology Stack

- Python
- Django
- Django REST Framework
- SQLite
- Django ORM
- Python Virtual Environment
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
│   ├── urls.py
│   └── ...
│
├── db.sqlite3
├── manage.py
├── requirements.txt
├── README.md
├── AI_USAGE.md
└── TEST_OUTPUT.md
