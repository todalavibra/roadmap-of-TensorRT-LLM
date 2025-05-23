import unittest
import sys
import os

# Adjust path to import from src
try:
    # Assumes tests are run from the project root (e.g., 'python -m unittest discover lifecycle_planner/tests')
    # or that lifecycle_planner is in PYTHONPATH
    from lifecycle_planner.src.product_definitions import get_product_data
except ImportError:
    # Fallback for running the test file directly from 'lifecycle_planner/tests'
    # or if 'lifecycle_planner' is not directly on the path.
    current_dir = os.path.dirname(os.path.abspath(__file__))  # .../lifecycle_planner/tests
    project_root = os.path.dirname(current_dir) # .../lifecycle_planner
    src_path = os.path.join(project_root, 'src') # .../lifecycle_planner/src
    # Add project_root to sys.path to allow 'from lifecycle_planner.src...'
    if project_root not in sys.path:
         sys.path.insert(0, project_root)
    # Add src_path to sys.path to allow direct 'from product_definitions...' (less ideal for packages)
    # if src_path not in sys.path:
    #    sys.path.insert(0, src_path)
    from lifecycle_planner.src.product_definitions import get_product_data


class TestProductDefinitions(unittest.TestCase):
    """
    Test cases for the product_definitions module.
    """
    def test_get_product_data_structure(self):
        """
        Tests the basic structure and presence of key elements in the data
        returned by get_product_data().
        """
        data = get_product_data()
        self.assertIsInstance(data, dict)
        self.assertIn("coffee_containers", data)
        self.assertIn("shopping_bags", data)
        self.assertIn("water_bottles", data)

        # Check one category in more detail (e.g., coffee_containers)
        coffee_data = data["coffee_containers"]
        self.assertIsInstance(coffee_data, list)
        self.assertGreater(len(coffee_data), 0, "Coffee containers list should not be empty.")

        # Check the structure of a sample product within that category
        sample_product = coffee_data[0]
        self.assertIsInstance(sample_product, dict)
        self.assertIn("name", sample_product)
        self.assertIn("type", sample_product)

        # Manufacturing Impact
        self.assertIn("manufacturing_impact", sample_product)
        self.assertIsInstance(sample_product["manufacturing_impact"], dict)
        self.assertIn("energy_mj", sample_product["manufacturing_impact"])
        self.assertIn("materials", sample_product["manufacturing_impact"]) # Added as per schema

        # Use Phase Impact
        self.assertIn("use_phase_impact", sample_product)
        self.assertIsInstance(sample_product["use_phase_impact"], dict)
        self.assertIn("lifespan_uses", sample_product["use_phase_impact"])
        self.assertIn("energy_per_use_mj", sample_product["use_phase_impact"]) # Added
        self.assertIn("waste_per_use_g", sample_product["use_phase_impact"]) # Added

        # End Of Life
        self.assertIn("end_of_life", sample_product)
        self.assertIsInstance(sample_product["end_of_life"], dict)
        self.assertIn("weight_g", sample_product["end_of_life"])
        self.assertIn("recyclable_locally", sample_product["end_of_life"]) # Added
        self.assertIn("actual_recycle_rate_percent", sample_product["end_of_life"]) # Added
        self.assertIn("disposal_path_notes", sample_product["end_of_life"]) # Added

if __name__ == '__main__':
    unittest.main()
