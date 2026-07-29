from decimal import Decimal
from typing import List, Tuple, Dict, Any, Optional, Union
from django.db.models import QuerySet
from .models import Order, Box, Product


def calculate_order_metrics(order_items: List[Dict[str, Any]]) -> Tuple[Decimal, Decimal, List[Dict[str, Any]], int]:
    """
    Calculates total weight, total volume, expands items by quantity, and counts total items.
    
    :param order_items: List of item dictionaries containing 'length', 'width', 'height', 'weight', and 'quantity'.
    :return: Tuple of (total_weight, total_volume, expanded_items_list, total_item_count)
    """
    total_weight = Decimal('0.00')
    total_volume = Decimal('0.00')
    expanded_items: List[Dict[str, Any]] = []
    total_item_count = 0

    for item in order_items:
        length = Decimal(str(item['length']))
        width = Decimal(str(item['width']))
        height = Decimal(str(item['height']))
        weight = Decimal(str(item['weight']))
        quantity = int(item.get('quantity', 1))

        if quantity < 1:
            continue

        item_volume = length * width * height
        item_total_weight = weight * Decimal(quantity)
        item_total_volume = item_volume * Decimal(quantity)

        total_weight += item_total_weight
        total_volume += item_total_volume
        total_item_count += quantity

        # Expand each product by quantity for spatial packing simulation
        for _ in range(quantity):
            expanded_items.append({
                'name': item.get('name', 'Product'),
                'length': float(length),
                'width': float(width),
                'height': float(height),
                'weight': weight,
                'volume': float(item_volume),
            })

    # Sort expanded items by volume in descending order (Largest First)
    expanded_items.sort(key=lambda x: x['volume'], reverse=True)

    return total_weight, total_volume, expanded_items, total_item_count


def get_orthogonal_rotations(length: float, width: float, height: float) -> List[Tuple[float, float, float]]:
    """
    Generates all unique 90-degree 3D orthogonal rotations for a rectangular item.
    
    :param length: Item length
    :param width: Item width
    :param height: Item height
    :return: List of unique (dx, dy, dz) dimension tuples.
    """
    all_rotations = [
        (length, width, height),
        (length, height, width),
        (width, length, height),
        (width, height, length),
        (height, length, width),
        (height, width, length),
    ]
    # Remove duplicate rotation configurations for cubes or symmetric boxes
    unique_rotations = list(set(all_rotations))
    return unique_rotations


def item_fits_in_box_dimensions(item: Dict[str, Any], box: Box) -> bool:
    """
    Quick check to verify if a single item can fit inside a box in at least one orientation.
    
    :param item: Item dict with float dimensions 'length', 'width', 'height'
    :param box: Box model instance
    :return: True if item fits in at least one orientation, False otherwise.
    """
    item_dims = sorted([item['length'], item['width'], item['height']])
    box_dims = sorted([
        float(box.internal_length), 
        float(box.internal_width), 
        float(box.internal_height)
    ])

    return (
        item_dims[0] <= box_dims[0] and
        item_dims[1] <= box_dims[1] and
        item_dims[2] <= box_dims[2]
    )


def boxes_overlap(
    pos1: Tuple[float, float, float], dim1: Tuple[float, float, float],
    pos2: Tuple[float, float, float], dim2: Tuple[float, float, float]
) -> bool:
    """
    Checks if two 3D bounding boxes overlap in space.
    
    :param pos1: (x, y, z) position of Box 1
    :param dim1: (dx, dy, dz) dimensions of Box 1
    :param pos2: (x, y, z) position of Box 2
    :param dim2: (dx, dy, dz) dimensions of Box 2
    :return: True if boxes overlap, False otherwise.
    """
    x1, y1, z1 = pos1
    dx1, dy1, dz1 = dim1

    x2, y2, z2 = pos2
    dx2, dy2, dz2 = dim2

    # Floating point tolerance
    epsilon = 1e-5

    return (
        x1 < x2 + dx2 - epsilon and x1 + dx1 > x2 + epsilon and
        y1 < y2 + dy2 - epsilon and y1 + dy1 > y2 + epsilon and
        z1 < z2 + dz2 - epsilon and z1 + dz1 > z2 + epsilon
    )


def can_pack_items_in_box(box: Box, expanded_items: List[Dict[str, Any]]) -> bool:
    """
    Attempts to pack all items into the given box using Extreme Point 3D First-Fit Decreasing packing.
    
    :param box: Box model instance
    :param expanded_items: List of individual expanded item dictionaries (sorted largest first)
    :return: True if all items can be packed without overlapping or exceeding box boundaries, False otherwise.
    """
    box_l = float(box.internal_length)
    box_w = float(box.internal_width)
    box_h = float(box.internal_height)

    # Placed items list: entries of (pos_tuple, dim_tuple)
    placed_items: List[Tuple[Tuple[float, float, float], Tuple[float, float, float]]] = []

    # Extreme points available for placement
    extreme_points: List[Tuple[float, float, float]] = [(0.0, 0.0, 0.0)]

    for item in expanded_items:
        rotations = get_orthogonal_rotations(item['length'], item['width'], item['height'])
        placed = False

        # Sort extreme points to encourage bottom-back-left packing (z ASC, y ASC, x ASC)
        extreme_points.sort(key=lambda pt: (pt[2], pt[1], pt[0]))

        for ep in list(extreme_points):
            ep_x, ep_y, ep_z = ep

            for dx, dy, dz in rotations:
                # Check boundary limits with floating-point tolerance
                if ep_x + dx > box_l + 1e-5 or ep_y + dy > box_w + 1e-5 or ep_z + dz > box_h + 1e-5:
                    continue

                # Check overlap against all already placed items
                overlap = False
                for placed_pos, placed_dim in placed_items:
                    if boxes_overlap((ep_x, ep_y, ep_z), (dx, dy, dz), placed_pos, placed_dim):
                        overlap = True
                        break

                if not overlap:
                    # Item fits at this extreme point with this rotation!
                    placed_items.append(((ep_x, ep_y, ep_z), (dx, dy, dz)))
                    placed = True

                    # Remove used extreme point
                    extreme_points.remove(ep)

                    # Generate 3 new extreme points from this placed item
                    new_pts = [
                        (ep_x + dx, ep_y, ep_z),
                        (ep_x, ep_y + dy, ep_z),
                        (ep_x, ep_y, ep_z + dz),
                    ]

                    for pt in new_pts:
                        # Only add point if within box boundaries and not already in extreme_points
                        if pt[0] < box_l and pt[1] < box_w and pt[2] < box_h and pt not in extreme_points:
                            extreme_points.append(pt)

                    break  # Break out of rotations loop

            if placed:
                break  # Break out of extreme points loop

        if not placed:
            # If an item could not be placed at any extreme point, packing fails for this box
            return False

    return True


def recommend_box_for_order(
    order_or_items: Union[Order, List[Dict[str, Any]]], 
    boxes: Optional[QuerySet] = None
) -> Dict[str, Any]:
    """
    Main service function to select the most suitable box for an order.
    
    Selection Strategy:
    1. Filter out boxes that exceed max weight capacity or total internal volume.
    2. Eliminate boxes where individual product dimensions exceed box dimensions.
    3. Perform 3D spatial packing simulation with 90-degree rotations.
    4. Select feasible box with:
       - Smallest internal volume (Primary)
       - Lowest cost (Secondary)
       - Lowest max weight capacity (Tertiary)
       - Smallest box ID (Deterministic Tie-breaker)
    
    :param order_or_items: Order model instance or list of item dicts with keys ('length', 'width', 'height', 'weight', 'quantity').
    :param boxes: Optional Django QuerySet of Box instances. Defaults to Box.objects.all().
    :return: Dictionary containing 'success', 'recommended_box', 'total_weight', 'total_item_volume', 'total_item_count', and 'reason'.
    """
    # 1. Extract items list depending on input type
    if isinstance(order_or_items, Order):
        order_items_data = [
            {
                'name': item.product.name,
                'length': item.product.length,
                'width': item.product.width,
                'height': item.product.height,
                'weight': item.product.weight,
                'quantity': item.quantity,
            }
            for item in order_or_items.items.select_related('product').all()
        ]
    else:
        order_items_data = order_or_items

    # 2. Handle empty orders
    if not order_items_data:
        return {
            'success': False,
            'recommended_box': None,
            'total_weight': Decimal('0.00'),
            'total_item_volume': Decimal('0.00'),
            'total_item_count': 0,
            'reason': 'Order contains no items.',
        }

    # 3. Calculate order total weight, total volume, and expanded items
    total_weight, total_volume, expanded_items, total_item_count = calculate_order_metrics(order_items_data)

    if not expanded_items or total_item_count == 0:
        return {
            'success': False,
            'recommended_box': None,
            'total_weight': Decimal('0.00'),
            'total_item_volume': Decimal('0.00'),
            'total_item_count': 0,
            'reason': 'Order items have invalid or zero quantities.',
        }

    # 4. Fetch candidate boxes
    if boxes is None:
        boxes = Box.objects.all()

    all_boxes = list(boxes)

    if not all_boxes:
        return {
            'success': False,
            'recommended_box': None,
            'total_weight': total_weight,
            'total_item_volume': total_volume,
            'total_item_count': total_item_count,
            'reason': 'No shipping boxes are registered in the warehouse system.',
        }

    feasible_boxes: List[Box] = []

    # 5. Fast Pre-Filtering & 3D Packing Verification
    for box in all_boxes:
        # Check weight capacity
        if total_weight > box.max_weight:
            continue

        # Check total volume
        box_volume = box.internal_length * box.internal_width * box.internal_height
        if total_volume > box_volume:
            continue

        # Check individual item dimension fitting
        individual_fit = True
        for item in expanded_items:
            if not item_fits_in_box_dimensions(item, box):
                individual_fit = False
                break

        if not individual_fit:
            continue

        # Perform 3D Spatial Packing Simulation
        if can_pack_items_in_box(box, expanded_items):
            feasible_boxes.append(box)

    # 6. Return result if no box is feasible
    if not feasible_boxes:
        return {
            'success': False,
            'recommended_box': None,
            'total_weight': total_weight,
            'total_item_volume': total_volume,
            'total_item_count': total_item_count,
            'reason': 'No suitable box found. Order exceeds weight, volume, or dimension boundaries of all available boxes.',
        }

    # 7. Sort feasible boxes according to criteria:
    #    1. Internal Volume ASC (Smallest box volume)
    #    2. Cost ASC (Cheaper box)
    #    3. Max Weight ASC
    #    4. ID ASC (Deterministic)
    feasible_boxes.sort(
        key=lambda b: (
            b.internal_length * b.internal_width * b.internal_height,
            b.cost,
            b.max_weight,
            b.id
        )
    )

    best_box = feasible_boxes[0]

    return {
        'success': True,
        'recommended_box': best_box,
        'total_weight': total_weight,
        'total_item_volume': total_volume,
        'total_item_count': total_item_count,
        'reason': f'Selected {best_box.name} as it is the smallest feasible box that fits the entire order.',
    }
