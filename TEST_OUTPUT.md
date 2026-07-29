# Test Output

## 1. Django System Check
- Command used: `.\venv\Scripts\python.exe manage.py check`
- Actual terminal output:
```
System check identified no issues (0 silenced).
```
- Status: PASS

## 2. Database Migration
- Command used: `.\venv\Scripts\python.exe manage.py migrate`
- Actual terminal output:
```
Operations to perform:
  Apply all migrations: admin, auth, box_selection, contenttypes, sessions
Running migrations:
  No migrations to apply.
```
- Status: PASS

## 3. Automated Tests
- Command used: `.\venv\Scripts\python.exe manage.py test box_selection.tests --verbosity=2`
- Actual terminal output:
```
Found 46 test(s).
Operations to perform:
  Synchronize unmigrated apps: messages, rest_framework, staticfiles
  Apply all migrations: admin, auth, box_selection, contenttypes, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_date... OK
  Applying admin.0004_logentry_remove_content_type... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_max_length... OK
  Applying auth.0005_alter_user_last_name_max_length... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_default_auto_field... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying box_selection.0001_initial... OK
  Applying sessions.0001_initial... OK
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
System check identified no issues (0 silenced).
test_create_box (box_selection.tests.BoxAPITests) ... ok
test_create_box_negative_internal_length (box_selection.tests.BoxAPITests) ... ok
test_create_box_zero_cost (box_selection.tests.BoxAPITests) ... ok
test_list_boxes (box_selection.tests.BoxAPITests) ... ok
test_retrieve_box (box_selection.tests.BoxAPITests) ... ok
test_retrieve_non_existent_box (box_selection.tests.BoxAPITests) ... ok
test_empty_order_recommendation (box_selection.tests.BoxRecommendationAPITests) ... ok
test_missing_order_id_get (box_selection.tests.BoxRecommendationAPITests) ... ok
test_missing_order_id_post (box_selection.tests.BoxRecommendationAPITests) ... ok
test_non_existent_order_recommendation (box_selection.tests.BoxRecommendationAPITests) ... ok
test_order_dimensions_exceed_all_boxes (box_selection.tests.BoxRecommendationAPITests) ... ok
test_order_fits_in_smallest_box (box_selection.tests.BoxRecommendationAPITests) ... ok
test_order_multiple_quantities_same_product (box_selection.tests.BoxRecommendationAPITests) ... ok
test_order_requires_larger_box (box_selection.tests.BoxRecommendationAPITests) ... ok
test_order_weight_exceeds_all_boxes (box_selection.tests.BoxRecommendationAPITests) ... ok
test_single_item_exactly_matching_box_dimensions (box_selection.tests.BoxRecommendationAPITests) ... ok
test_tie_breaking_cheaper_box_wins (box_selection.tests.BoxRecommendationAPITests) ... ok
test_tie_breaking_lower_max_weight_wins (box_selection.tests.BoxRecommendationAPITests) ... ok
test_tie_breaking_smallest_id_wins (box_selection.tests.BoxRecommendationAPITests) ... ok
test_empty_order (box_selection.tests.BoxSelectionServiceTests) ... ok
test_heavy_item_selects_heavy_duty_box (box_selection.tests.BoxSelectionServiceTests) ... ok
test_no_suitable_box_when_exceeding_all_capacities (box_selection.tests.BoxSelectionServiceTests) ... ok
test_product_rotation_selection (box_selection.tests.BoxSelectionServiceTests) ... ok
test_quantity_expansion_and_weight_limit (box_selection.tests.BoxSelectionServiceTests) ... ok
test_single_item_fits_in_smallest_box (box_selection.tests.BoxSelectionServiceTests) ... ok
test_create_order_empty_items (box_selection.tests.OrderAPITests) ... ok
test_create_order_invalid_product_id (box_selection.tests.OrderAPITests) ... ok
test_create_order_missing_items (box_selection.tests.OrderAPITests) ... ok
test_create_order_negative_quantity (box_selection.tests.OrderAPITests) ... ok
test_create_order_quantity_zero (box_selection.tests.OrderAPITests) ... ok
test_create_order_with_valid_items (box_selection.tests.OrderAPITests) ... ok
test_retrieve_non_existent_order (box_selection.tests.OrderAPITests) ... ok
test_retrieve_order (box_selection.tests.OrderAPITests) ... ok
test_create_product (box_selection.tests.ProductAPITests) ... ok
test_create_product_missing_field (box_selection.tests.ProductAPITests) ... ok
test_create_product_negative_length (box_selection.tests.ProductAPITests) ... ok
test_create_product_zero_weight (box_selection.tests.ProductAPITests) ... ok
test_list_products (box_selection.tests.ProductAPITests) ... ok
test_retrieve_non_existent_product (box_selection.tests.ProductAPITests) ... ok
test_retrieve_product (box_selection.tests.ProductAPITests) ... ok
test_box_serializer_invalid_cost_or_weight (box_selection.tests.SerializerTests) ... ok
test_box_serializer_valid (box_selection.tests.SerializerTests) ... ok
test_order_serializer_creation (box_selection.tests.SerializerTests) ... ok
test_order_serializer_empty_items_invalid (box_selection.tests.SerializerTests) ... ok
test_product_serializer_invalid_dimensions (box_selection.tests.SerializerTests) ... ok
test_product_serializer_valid (box_selection.tests.SerializerTests) ... ok

----------------------------------------------------------------------
Ran 46 tests in 0.249s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
```
- Number of tests executed: 46
- Status: PASS

## 4. Development Server
- Command used: `.\venv\Scripts\python.exe manage.py runserver`
- Result of starting the server:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
- Status: PASS
