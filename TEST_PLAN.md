# Test Plan — Box Selection REST API

## 1. Product API

| Test Name | Input | Expected Output / Status Code |
|-----------|-------|------------------------------|
| Create product (valid) | `POST /api/products/` with valid `name`, `length`, `width`, `height`, `weight` | `201 Created`, returns created product object with `id` |
| List products | `GET /api/products/` | `200 OK`, returns list of products |
| Retrieve product by ID | `GET /api/products/<id>/` for existing product | `200 OK`, returns product object |
| Retrieve non-existent product | `GET /api/products/9999/` | `404 Not Found`, `{"detail": "Product not found."}` |
| Create product with negative length | `POST /api/products/` with `length: -5` | `400 Bad Request`, `{"length": ["Length must be greater than zero."]}` |
| Create product with missing required field | `POST /api/products/` with only `name` | `400 Bad Request`, field-level error for missing dimension/weight |
| Create product with zero weight | `POST /api/products/` with `weight: 0` | `400 Bad Request`, `{"weight": ["Weight must be greater than zero."]}` |

## 2. Box API

| Test Name | Input | Expected Output / Status Code |
|-----------|-------|------------------------------|
| Create box (valid) | `POST /api/boxes/` with valid `name`, `internal_length`, `internal_width`, `internal_height`, `max_weight`, `cost` | `201 Created`, returns created box object with `id` |
| List boxes | `GET /api/boxes/` | `200 OK`, returns list of boxes |
| Retrieve box by ID | `GET /api/boxes/<id>/` for existing box | `200 OK`, returns box object |
| Retrieve non-existent box | `GET /api/boxes/9999/` | `404 Not Found`, `{"detail": "Box not found."}` |
| Create box with negative internal length | `POST /api/boxes/` with `internal_length: -10` | `400 Bad Request`, `{"internal_length": ["Internal length must be greater than zero."]}` |
| Create box with zero cost | `POST /api/boxes/` with `cost: 0` | `400 Bad Request`, `{"cost": ["Cost must be greater than zero."]}` |

## 3. Order API

| Test Name | Input | Expected Output / Status Code |
|-----------|-------|------------------------------|
| Create order with valid items | `POST /api/orders/` with `items: [{product_id: 1, quantity: 2}]` | `201 Created`, returns order with nested `items` |
| Retrieve order by ID | `GET /api/orders/<id>/` for existing order | `200 OK`, returns order with nested items and product details |
| Create order with invalid product_id | `POST /api/orders/` with `items: [{product_id: 9999, quantity: 1}]` | `400 Bad Request`, `{"items": [{"product_id": ["Invalid pk \"9999\" - object does not exist."]}]}` |
| Create order with empty items list | `POST /api/orders/` with `items: []` | `400 Bad Request`, `{"items": ["An order must contain at least one item."]}` |
| Create order with missing items field | `POST /api/orders/` with no `items` key | `400 Bad Request`, `{"items": ["This field is required."]}` |
| Create order with quantity zero | `POST /api/orders/` with `items: [{product_id: 1, quantity: 0}]` | `400 Bad Request`, `{"items": [{"quantity": ["Ensure this value is greater than or equal to 1."]}]}` |
| Create order with negative quantity | `POST /api/orders/` with `items: [{product_id: 1, quantity: -1}]` | `400 Bad Request`, `{"items": [{"quantity": ["Ensure this value is greater than or equal to 1."]}]}` |
| Retrieve non-existent order | `GET /api/orders/9999/` | `404 Not Found`, `{"detail": "Order not found."}` |

## 4. Box Recommendation API

| Test Name | Input | Expected Output / Status Code |
|-----------|-------|------------------------------|
| Order fits in smallest box | `GET /api/orders/<id>/recommend-box/` where order total weight/volume fit the smallest available box | `200 OK`, `success: true`, `recommended_box` is the smallest box, reason indicates smallest feasible box |
| Order requires a larger box | `GET /api/orders/<id>/recommend-box/` where order exceeds smallest box but fits a larger one | `200 OK`, `success: true`, `recommended_box` is the next larger feasible box |
| Order total weight exceeds all boxes | `GET /api/orders/<id>/recommend-box/` where combined weight > every box `max_weight` | `200 OK`, `success: false`, `recommended_box: null`, reason mentions weight boundaries |
| Item dimensions don't fit any box even after rotation | `GET /api/orders/<id>/recommend-box/` where one item is larger than every box in all orientations | `200 OK`, `success: false`, `recommended_box: null`, reason mentions dimension boundaries |
| Order with multiple quantities of same product | `GET /api/orders/<id>/recommend-box/` where order has `quantity: 5` for one product | `200 OK`, `success` depends on feasibility; `total_item_count` reflects expanded quantity |
| Non-existent order ID | `GET /api/orders/9999/recommend-box/` | `404 Not Found`, `{"error": "Order not found."}` |
| Missing order ID (GET query param) | `GET /api/orders/recommend-box/` without `order_id` | `400 Bad Request`, `{"error": "Order ID is required."}` |
| Missing order ID (POST body) | `POST /api/orders/recommend-box/` with empty body | `400 Bad Request`, `{"error": "Order ID is required."}` |

## 5. Edge Cases

| Test Name | Input | Expected Output / Status Code |
|-----------|-------|------------------------------|
| Empty order recommendation | `GET /api/orders/<id>/recommend-box/` for an order with no items | `200 OK`, `success: false`, `recommended_box: null`, reason: `"Order contains no items."` |
| Single item exactly matching box dimensions | `GET /api/orders/<id>/recommend-box/` where item dimensions equal box internal dimensions exactly | `200 OK`, `success: true`, item fits in that box, reason indicates selected box |
| Tie-breaking between equally-sized boxes (cheaper wins) | Two boxes with identical internal volume but different `cost`; order fits both | `200 OK`, `success: true`, `recommended_box` is the box with lower `cost` |
| Tie-breaking between equally-sized and equally-priced boxes (lower max weight wins) | Two boxes with same volume and cost but different `max_weight`; order fits both | `200 OK`, `success: true`, `recommended_box` is the box with lower `max_weight` |
| Tie-breaking between identical boxes (smallest ID wins) | Two boxes with same volume, cost, and max weight; order fits both | `200 OK`, `success: true`, `recommended_box` is the box with smaller `id` |
