PRODUCT_CATEGORIES = {
    "coffee_containers": [
        {
            "name": "Disposable Paper Cup (12oz, w/lid)",
            "type": "disposable",
            "manufacturing_impact": {
                "energy_mj": 0.55,  # Includes cup and lid production
                "materials": "Paper (virgin or recycled), PLA or PE lining, Plastic lid (PS or PET)"
            },
            "use_phase_impact": {
                "lifespan_uses": 1,
                "energy_per_use_mj": 0.0, # No energy use beyond manufacturing/disposal
                "waste_per_use_g": 15.0 # Approx weight of cup (10g) + lid (5g)
            },
            "end_of_life": {
                "weight_g": 15.0,
                "recyclable_locally": False, # Plastic lining makes it hard, lids often not accepted
                "actual_recycle_rate_percent": 2.0, # Very low due to contamination and lining
                "disposal_path_notes": "Mostly landfilled; some composting facilities accept PLA-lined cups if clean."
            }
        },
        {
            "name": "Reusable Ceramic Mug (12oz)",
            "type": "reusable",
            "manufacturing_impact": {
                "energy_mj": 18.0, # Varies greatly based on production (e.g., kiln efficiency)
                "materials": "Clay (earthenware, stoneware, or porcelain), Glaze"
            },
            "use_phase_impact": {
                "lifespan_uses": 1000, # Assumption
                "energy_per_use_mj": 0.15, # Approx. for dishwasher (shared load) or handwashing with hot water
                "waste_per_use_g": 0.0 # Assuming no waste generated per use until end of life
            },
            "end_of_life": {
                "weight_g": 350.0, # Average weight
                "recyclable_locally": False, # Ceramics generally not recycled in household systems
                "actual_recycle_rate_percent": 0.0,
                "disposal_path_notes": "Landfilled; can be broken up for aggregate in some specific projects."
            }
        },
        {
            "name": "Reusable Insulated Travel Mug (12oz, Stainless)",
            "type": "reusable",
            "manufacturing_impact": {
                "energy_mj": 35.0, # Higher due to stainless steel and plastic components
                "materials": "Stainless Steel (body), Plastic (lid, handle), Silicone (seal)"
            },
            "use_phase_impact": {
                "lifespan_uses": 1500, # Assumption, durable item
                "energy_per_use_mj": 0.15, # Similar to ceramic mug for washing
                "waste_per_use_g": 0.0
            },
            "end_of_life": {
                "weight_g": 250.0, # Average weight
                "recyclable_locally": True, # Stainless steel part is highly recyclable if disassembled
                "actual_recycle_rate_percent": 20.0, # Lower if not disassembled, plastic parts often not recycled
                "disposal_path_notes": "Steel part recyclable if separated from plastic. Otherwise landfilled."
            }
        }
    ],
    "shopping_bags": [
        {
            "name": "Single-use Plastic Bag (HDPE)",
            "type": "disposable",
            "manufacturing_impact": {"energy_mj": 0.1, "materials": "High-Density Polyethylene (HDPE)"},
            "use_phase_impact": {"lifespan_uses": 1, "energy_per_use_mj": 0.0, "waste_per_use_g": 5.0},
            "end_of_life": {"weight_g": 5.0, "recyclable_locally": True, "actual_recycle_rate_percent": 5.0, "disposal_path_notes": "Often landfilled, becomes litter, some store drop-off recycling programs."}
        },
        {
            "name": "Reusable Polypropylene Bag (NWPP)",
            "type": "reusable",
            "manufacturing_impact": {"energy_mj": 0.5, "materials": "Non-Woven Polypropylene (NWPP)"}, # Placeholder, actual value is higher
            "use_phase_impact": {"lifespan_uses": 50, "energy_per_use_mj": 0.0, "waste_per_use_g": 0.0}, # Placeholder for uses
            "end_of_life": {"weight_g": 60.0, "recyclable_locally": False, "actual_recycle_rate_percent": 1.0, "disposal_path_notes": "Typically landfilled; some specialized recyclers exist but uncommon."} # Placeholder
        },
        {
            "name": "Reusable Cotton Bag",
            "type": "reusable",
            "manufacturing_impact": {"energy_mj": 20.0, "materials": "Cotton (conventional or organic)"}, # Placeholder, can be very high for conventional
            "use_phase_impact": {"lifespan_uses": 150, "energy_per_use_mj": 0.1, "waste_per_use_g": 0.0}, # Placeholder for uses, washing energy
            "end_of_life": {"weight_g": 150.0, "recyclable_locally": False, "actual_recycle_rate_percent": 0.0, "disposal_path_notes": "Landfilled or compostable if 100% natural cotton and no dyes/prints."} # Placeholder
        }
    ],
    "water_bottles": [
        {
            "name": "Single-use PET Plastic Bottle (500ml)",
            "type": "disposable",
            "manufacturing_impact": {"energy_mj": 2.5, "materials": "Polyethylene Terephthalate (PET), Plastic cap (HDPE/PP)"}, # Placeholder, varies
            "use_phase_impact": {"lifespan_uses": 1, "energy_per_use_mj": 0.0, "waste_per_use_g": 20.0}, # Placeholder, weight of bottle + cap
            "end_of_life": {"weight_g": 20.0, "recyclable_locally": True, "actual_recycle_rate_percent": 29.0, "disposal_path_notes": "Widely recycled but still significant landfill/litter."} # Placeholder
        },
        {
            "name": "Reusable Tritan Plastic Bottle (500ml)",
            "type": "reusable",
            "manufacturing_impact": {"energy_mj": 10.0, "materials": "Tritan Copolyester, Plastic cap (PP)"}, # Placeholder
            "use_phase_impact": {"lifespan_uses": 500, "energy_per_use_mj": 0.05, "waste_per_use_g": 0.0}, # Placeholder for uses, washing energy
            "end_of_life": {"weight_g": 150.0, "recyclable_locally": False, "actual_recycle_rate_percent": 1.0, "disposal_path_notes": "Generally landfilled; Tritan is #7 plastic, hard to recycle."} # Placeholder
        },
        {
            "name": "Reusable Stainless Steel Bottle (500ml)",
            "type": "reusable",
            "manufacturing_impact": {"energy_mj": 30.0, "materials": "Stainless Steel, Plastic/Silicone cap components"}, # Placeholder
            "use_phase_impact": {"lifespan_uses": 2000, "energy_per_use_mj": 0.1, "waste_per_use_g": 0.0}, # Placeholder for uses, washing energy
            "end_of_life": {"weight_g": 300.0, "recyclable_locally": True, "actual_recycle_rate_percent": 20.0, "disposal_path_notes": "Steel part recyclable if separated. Otherwise landfilled."} # Placeholder
        }
    ]
}

def get_product_data():
    """
    Returns the main dictionary containing all product category data.
    """
    return PRODUCT_CATEGORIES

if __name__ == '__main__':
    # Example of accessing the data
    all_data = get_product_data()
    
    print("--- Coffee Containers ---")
    for item in all_data["coffee_containers"]:
        print(f"  Name: {item['name']}")
        print(f"    Manufacturing Energy: {item['manufacturing_impact']['energy_mj']} MJ")
        print(f"    Lifespan (uses): {item['use_phase_impact']['lifespan_uses']}")
        print(f"    Weight: {item['end_of_life']['weight_g']}g")

    print("\n--- Shopping Bags (Example - First Item) ---")
    if all_data["shopping_bags"]:
        first_bag = all_data["shopping_bags"][0]
        print(f"  Name: {first_bag['name']}")
        print(f"    Type: {first_bag['type']}")
        print(f"    Materials: {first_bag['manufacturing_impact']['materials']}")
        print(f"    Recyclable Locally: {first_bag['end_of_life']['recyclable_locally']}")

    print("\n--- Water Bottles (Example - First Item) ---")
    if all_data["water_bottles"]:
        first_bottle = all_data["water_bottles"][0]
        print(f"  Name: {first_bottle['name']}")
        print(f"    Type: {first_bottle['type']}")
        print(f"    Manufacturing Energy: {first_bottle['manufacturing_impact']['energy_mj']} MJ")
        print(f"    Actual Recycle Rate: {first_bottle['end_of_life']['actual_recycle_rate_percent']}%")

    # Test a placeholder value
    print("\n--- Testing Placeholder in Cotton Bag ---")
    cotton_bag = next((bag for bag in all_data["shopping_bags"] if bag["name"] == "Reusable Cotton Bag"), None)
    if cotton_bag:
        print(f"  Cotton Bag Lifespan Uses: {cotton_bag['use_phase_impact']['lifespan_uses']}") # Expected: 150 (placeholder)
        print(f"  Cotton Bag Disposal Notes: {cotton_bag['end_of_life']['disposal_path_notes']}") # Expected: Landfilled or compostable...
    else:
        print("Cotton bag not found for placeholder test.")
