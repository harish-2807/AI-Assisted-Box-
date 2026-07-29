# AI Usage

## 1. AI Tools Used

The following AI tools were used during the development of this assignment:

- ChatGPT
- CodeGPT Chat in VS Code

The AI tools were used for project planning, understanding the requirements, designing the box selection algorithm, generating code, debugging, and reviewing implementation decisions.

---

## 2. Prompts Used

The following prompts were used during the development process.

### Prompt 1: Django Project Setup

I asked the AI to help set up a Django project with Django REST Framework and the required dependencies for the box selection assignment.

### Prompt 2: Database Models

I asked the AI to create Django models for:

- Product
- Box
- Order
- OrderItem

The models were designed based on the dimensions, weight, capacity, cost, and order requirements in the assignment.

### Prompt 3: Django Admin

I asked the AI to configure Django Admin for managing products, boxes, orders, and order items.

### Prompt 4: Box Selection Algorithm Design

I asked the AI to analyze the box selection problem and propose an algorithm that considers:

- Product dimensions
- Product weight
- Product quantities
- Box dimensions
- Box weight capacity
- Product rotation
- Multiple products
- 3D packing
- Box selection criteria

The AI proposed a multi-phase filtering and 3D packing approach.

### Prompt 5: Box Selection Service

I asked the AI to implement the box selection business logic in a dedicated service layer.

The service was designed to:

- Calculate total order weight
- Calculate total product volume
- Filter unsuitable boxes
- Consider product orientations
- Handle product quantities
- Check 3D packing feasibility
- Select a recommended box

### Prompt 6: Django REST Framework Serializers

I asked the AI to create serializers for:

- Product
- Box
- Order
- OrderItem

The serializers were required to validate input values, product references, quantities, and order items.

### Prompt 7: REST API Views

I asked the AI to implement REST API views for products, boxes, orders, and the box recommendation functionality.

---

## 3. AI Output Accepted

After reviewing the generated output, I accepted useful parts of the AI-generated implementation, including:

- Django project structure
- Django model implementation
- Database migrations
- Django Admin configuration
- Box selection algorithm design
- Service-layer approach for box selection
- Django REST Framework serializers
- Input validation
- Automated test structure

The generated code was reviewed against the assignment requirements before being accepted.

---

## 4. AI Output Rejected or Modified

Some AI-generated suggestions were reviewed and modified.

### Box Selection Priority

The AI initially proposed selecting the lowest-cost feasible box as the primary criterion.

I modified the selection criteria to prioritize:

1. Smallest feasible box by internal volume
2. Lowest cost when box volumes are equal
3. Additional deterministic tie-breakers when required

This was chosen to reduce unused space and packaging material.

### "Optimal Box" Terminology

The AI used the term "Optimal Box."

I changed this terminology to "Recommended Box" because the 3D packing approach is heuristic and does not mathematically guarantee a globally optimal packing solution.

### AI-Generated Code Review

AI-generated code was not automatically accepted without review. Code was checked against the assignment requirements and modified where necessary.

---

## 5. Mistakes or Issues Found

During development, the following issues were identified:

### Python Environment / Pylance Import Warnings

VS Code initially showed unresolved import warnings for Django and Django REST Framework.

The issue was related to the Python interpreter/environment selected by VS Code.

The project virtual environment was configured and the project was verified using Django system checks.

### Zero Tests Discovered

At one stage, running:

python manage.py test

returned:

Ran 0 tests in 0.000s - OK

This was identified as an issue because a successful test command with zero discovered tests does not provide meaningful test coverage.

Additional test cases were added and the test suite was reviewed to ensure that tests were actually being discovered and executed.

### AI Service Error

During development, CodeGPT returned a Vertex AI error:

429 RESOURCE_EXHAUSTED

This was an AI service limitation and was not caused by the Django application code.

The project development was continued by adjusting prompts and using smaller, more focused requests when necessary.

---

## 6. Verification Steps

The generated and modified code was verified using the following steps:

### Django System Check

```text
python manage.py check