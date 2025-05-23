import math

try:
    from .product_definitions import get_product_data
except ImportError:
    # Fallback for standalone execution or if module structure isn't recognized
    from product_definitions import get_product_data

def calculate_annual_impact(product_info: dict, usage_per_day: int, days_per_year: int = 365) -> dict:
    """
    Calculates the estimated annual environmental impact of a single product type
    based on usage frequency.

    Args:
        product_info: A dictionary containing the product's lifecycle data.
        usage_per_day: How many times the product category is used per day
                       (e.g., 2 cups of coffee per day).
        days_per_year: Number of days in a year the usage occurs.

    Returns:
        A dictionary summarizing the annual impact.
    """
    total_uses_per_year = usage_per_day * days_per_year
    num_items_needed = 0
    annual_manufacturing_energy = 0.0
    annual_use_energy = 0.0
    annual_waste_g = 0.0

    # Ensure 'actual_recycle_rate_percent' exists, default to 0 if not
    actual_recycle_rate = product_info['end_of_life'].get('actual_recycle_rate_percent', 0) / 100.0

    if product_info['type'] == "disposable":
        num_items_needed = total_uses_per_year
        annual_manufacturing_energy = num_items_needed * product_info['manufacturing_impact']['energy_mj']
        annual_use_energy = num_items_needed * product_info['use_phase_impact']['energy_per_use_mj']
        
        # Waste from each item that is not recycled
        waste_per_item_at_eol_g = product_info['end_of_life']['weight_g'] * (1 - actual_recycle_rate)
        annual_waste_g = num_items_needed * waste_per_item_at_eol_g
    
    elif product_info['type'] == "reusable":
        lifespan_uses = product_info['use_phase_impact']['lifespan_uses']
        if lifespan_uses <= 0: # Avoid division by zero or negative lifespan
            lifespan_uses = 1 
            
        num_items_needed = math.ceil(total_uses_per_year / lifespan_uses)
        annual_manufacturing_energy = num_items_needed * product_info['manufacturing_impact']['energy_mj']
        # For reusable items, use energy is per actual use, not per item manufactured
        annual_use_energy = total_uses_per_year * product_info['use_phase_impact']['energy_per_use_mj']
        
        # Waste from each item at the end of its life, considering how many items are consumed annually
        waste_per_item_at_eol_g = product_info['end_of_life']['weight_g'] * (1 - actual_recycle_rate)
        annual_waste_g = num_items_needed * waste_per_item_at_eol_g
    else:
        # Should not happen with current data, but good to handle
        print(f"Warning: Unknown product type '{product_info['type']}' for product '{product_info['name']}'. Skipping.")
        return {} # Or raise an error

    total_annual_energy_mj = annual_manufacturing_energy + annual_use_energy

    return {
        "product_name": product_info['name'],
        "num_items_per_year": num_items_needed,
        "total_annual_energy_mj": round(total_annual_energy_mj, 2),
        "total_annual_waste_g": round(annual_waste_g, 2),
        "details": {
            "annual_manufacturing_energy_mj": round(annual_manufacturing_energy, 2),
            "annual_use_phase_energy_mj": round(annual_use_energy, 2),
            "items_become_waste_annually_g": round(annual_waste_g, 2)
        }
    }

def compare_products(category_name: str, usage_per_day: int, days_per_year: int = 365) -> list[dict]:
    """
    Compares products within a given category based on annual impact.

    Args:
        category_name: The key for the product category in PRODUCT_CATEGORIES.
        usage_per_day: How many times the product category is used per day.
        days_per_year: Number of days in a year the usage occurs.

    Returns:
        A list of dictionaries, where each dictionary is the result from
        calculate_annual_impact for a product in the category.
    """
    all_data = get_product_data()
    products_in_category = all_data.get(category_name)

    if products_in_category is None:
        print(f"Error: Category '{category_name}' not found.")
        return []

    comparison_results = []
    for product_data_item in products_in_category:
        impact = calculate_annual_impact(product_data_item, usage_per_day, days_per_year)
        if impact: # Only append if impact calculation was successful
            comparison_results.append(impact)
    
    return comparison_results

if __name__ == '__main__':
    print("--- Comparing Coffee Containers (Usage: 2 per day, 365 days/year) ---")
    coffee_comparison = compare_products("coffee_containers", usage_per_day=2, days_per_year=365)
    for result in coffee_comparison:
        print(f"\n  Product: {result['product_name']}")
        print(f"    Items needed per year: {result['num_items_per_year']}")
        print(f"    Total Annual Energy: {result['total_annual_energy_mj']} MJ")
        print(f"    Total Annual Waste: {result['total_annual_waste_g']} g")
        print(f"    Details:")
        print(f"      Manufacturing Energy: {result['details']['annual_manufacturing_energy_mj']} MJ")
        print(f"      Use Phase Energy: {result['details']['annual_use_phase_energy_mj']} MJ")
        print(f"      Waste Generated (EOL): {result['details']['items_become_waste_annually_g']} g")

    print("\n--- Comparing Shopping Bags (Usage: 1 per day, 52 days/year, e.g. weekly shopping) ---")
    # Assuming 1 "major" shopping trip per week where a bag choice is made
    # And let's say on average one uses 5 bags of the chosen type for that trip.
    # So, usage_per_day for this scenario is more like "uses of the category per relevant day".
    # If one "shopping day" uses 5 plastic bags, then usage_per_day = 5, days_per_year = 52.
    bags_comparison = compare_products("shopping_bags", usage_per_day=5, days_per_year=52)
    for result in bags_comparison:
        print(f"\n  Product: {result['product_name']}")
        print(f"    Items needed per year: {result['num_items_per_year']}")
        print(f"    Total Annual Energy: {result['total_annual_energy_mj']} MJ")
        print(f"    Total Annual Waste: {result['total_annual_waste_g']} g")

    print("\n--- Comparing Water Bottles (Usage: 3 per day, 200 days/year, e.g. work/school days) ---")
    bottles_comparison = compare_products("water_bottles", usage_per_day=3, days_per_year=200)
    for result in bottles_comparison:
        print(f"\n  Product: {result['product_name']}")
        print(f"    Items needed per year: {result['num_items_per_year']}")
        print(f"    Total Annual Energy: {result['total_annual_energy_mj']} MJ")
        print(f"    Total Annual Waste: {result['total_annual_waste_g']} g")

    print("\n--- Test: Category not found ---")
    non_existent_comparison = compare_products("non_existent_category", 1)
    print(f"Result for non-existent category: {non_existent_comparison}")

    print("\n--- Test: Reusable with lifespan_uses = 0 (should default to 1) ---")
    # Create a mock product to test this edge case without altering product_definitions
    mock_reusable_zero_lifespan = {
        "name": "Mock Reusable Zero Lifespan",
        "type": "reusable",
        "manufacturing_impact": {"energy_mj": 10.0, "materials": "Mock"},
        "use_phase_impact": {"lifespan_uses": 0, "energy_per_use_mj": 0.1, "waste_per_use_g": 0.0},
        "end_of_life": {"weight_g": 100.0, "recyclable_locally": False, "actual_recycle_rate_percent": 0.0, "disposal_path_notes": "Mock"}
    }
    impact_zero_lifespan = calculate_annual_impact(mock_reusable_zero_lifespan, usage_per_day=1, days_per_year=10)
    if impact_zero_lifespan: # Check if calculation was successful
        print(f"  Product: {impact_zero_lifespan['product_name']}")
        print(f"    Items needed per year: {impact_zero_lifespan['num_items_per_year']}") # Should be 10 (10 uses / 1 lifespan_use)
        expected_items = 10
        if impact_zero_lifespan['num_items_per_year'] == expected_items:
            print(f"    Test PASSED for num_items_per_year (expected {expected_items})")
        else:
            print(f"    Test FAILED for num_items_per_year (expected {expected_items}, got {impact_zero_lifespan['num_items_per_year']})")
    else:
        print("    Test FAILED for zero lifespan reusable: No impact data returned.")
