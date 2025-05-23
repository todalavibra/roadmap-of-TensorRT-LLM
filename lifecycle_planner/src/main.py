import argparse

try:
    from .comparison_logic import compare_products
    from .product_definitions import get_product_data
except ImportError:
    # Fallback for running main.py directly for testing,
    # assuming comparison_logic.py and product_definitions.py are in the same directory or PYTHONPATH.
    from comparison_logic import compare_products
    from product_definitions import get_product_data

def setup_arg_parser():
    """
    Sets up the argument parser for the command-line interface.
    """
    try:
        available_categories = list(get_product_data().keys())
    except Exception as e:
        # This might happen if product_definitions.py is not found or has errors
        print(f"Critical Error: Could not load product categories. {e}")
        available_categories = [] # Allow argparse to still run, but choices will be empty

    parser = argparse.ArgumentParser(description="Compare lifecycle impacts of common products.")
    
    parser.add_argument(
        "category",
        help="Category of products to compare.",
        choices=available_categories,
        metavar="CATEGORY" # More descriptive in help message
    )
    parser.add_argument(
        "usage_per_day",
        type=int,
        help="Your daily usage for this category (e.g., 2 for 2 coffees/day).",
        metavar="USAGE_PER_DAY"
    )
    parser.add_argument(
        "--days_per_year", "-d",
        type=int,
        default=365,
        help="Number of days for the annual impact calculation (default: 365).",
        metavar="DAYS"
    )

    # Basic input validation for positive numbers
    args = parser.parse_args()
    if args.usage_per_day <= 0:
        parser.error("usage_per_day must be a positive integer.")
    if args.days_per_year <= 0:
        parser.error("days_per_year must be a positive integer.")
        
    return args

def main():
    """
    Main function to run the CLI application.
    """
    args = setup_arg_parser()

    # Check if available_categories was empty during setup_arg_parser
    if not get_product_data().keys():
        # Error message already printed by setup_arg_parser, or compare_products will handle it.
        # This is a safeguard.
        print("Exiting due to missing product category data.")
        return

    results = compare_products(args.category, args.usage_per_day, args.days_per_year)

    if not results:
        # compare_products prints its own error if category not found.
        # This handles other unexpected empty results.
        print(f"\nNo comparison data found for category '{args.category}' or an error occurred during comparison.")
    else:
        print(f"\n--- Comparison for Category: {args.category} ---")
        print(f"--- Assuming daily usage of: {args.usage_per_day} items/uses for {args.days_per_year} days per year ---")

        for product_impact in results:
            if not product_impact: # Skip if an individual product calculation failed
                print("\n--- Error processing one product ---")
                continue

            print(f"\n--- Product: {product_impact['product_name']} ---")
            print(f"  Items needed per year: {product_impact['num_items_per_year']}")
            print(f"  Total Annual Energy: {product_impact['total_annual_energy_mj']:.2f} MJ")
            
            waste_g = product_impact['total_annual_waste_g']
            waste_kg = waste_g / 1000.0
            print(f"  Total Annual Waste: {waste_g:.2f} g ({waste_kg:.2f} kg)")

            if 'details' in product_impact:
                details = product_impact['details']
                print(f"    Manufacturing Energy: {details.get('annual_manufacturing_energy_mj', 0.0):.2f} MJ")
                print(f"    Use Phase Energy: {details.get('annual_use_phase_energy_mj', 0.0):.2f} MJ")
                # The 'items_become_waste_annually_g' is essentially the total_annual_waste_g,
                # so no need to repeat unless it has a different specific meaning in some context.
                # print(f"    Waste from EOL items: {details.get('items_become_waste_annually_g', 0.0):.2f} g")
            else:
                print("    (No detailed breakdown available)")

        print("\n--- End of Comparison ---")

if __name__ == "__main__":
    main()
