import unittest
import math
from unittest.mock import patch
import sys
import os

# Adjust path to import from src
try:
    # Assumes tests are run from the project root
    from lifecycle_planner.src.comparison_logic import calculate_annual_impact, compare_products
    # from lifecycle_planner.src.product_definitions import get_product_data # Not directly used in every test, but contextually relevant
except ImportError:
    # Fallback for running the test file directly from 'lifecycle_planner/tests'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    src_path = os.path.join(project_root, 'src')
    if project_root not in sys.path: # Add project root to find 'lifecycle_planner.src'
        sys.path.insert(0, project_root)
    # if src_path not in sys.path: # Alternative: add src itself to find modules directly
    #    sys.path.insert(0, src_path)
    from lifecycle_planner.src.comparison_logic import calculate_annual_impact, compare_products


class TestComparisonLogic(unittest.TestCase):
    """
    Test cases for the comparison_logic module.
    """

    def test_calculate_annual_impact_disposable(self):
        """Test annual impact calculation for a disposable item."""
        product_info = {
            "name": "Test Disposable", "type": "disposable",
            "manufacturing_impact": {"energy_mj": 0.5},
            "use_phase_impact": {"energy_per_use_mj": 0.01, "lifespan_uses": 1, "waste_per_use_g": 0.0}, # Added waste_per_use_g
            "end_of_life": {"weight_g": 10.0, "actual_recycle_rate_percent": 10.0}
        }
        impact = calculate_annual_impact(product_info, usage_per_day=2, days_per_year=10)
        
        self.assertEqual(impact["product_name"], "Test Disposable")
        self.assertEqual(impact["num_items_per_year"], 20)  # 2 * 10
        
        expected_mfg_energy = 20 * 0.5
        expected_use_energy = 20 * 0.01
        self.assertAlmostEqual(impact["total_annual_energy_mj"], expected_mfg_energy + expected_use_energy)
        
        expected_waste_per_item_eol = 10.0 * (1 - 0.10)  # 9g
        self.assertAlmostEqual(impact["total_annual_waste_g"], 20 * expected_waste_per_item_eol)
        
        self.assertAlmostEqual(impact["details"]["annual_manufacturing_energy_mj"], expected_mfg_energy)
        self.assertAlmostEqual(impact["details"]["annual_use_phase_energy_mj"], expected_use_energy)
        self.assertAlmostEqual(impact["details"]["items_become_waste_annually_g"], 20 * expected_waste_per_item_eol)


    def test_calculate_annual_impact_reusable_single_item_lifespan(self):
        """Test impact for a reusable item whose lifespan covers all uses in a year."""
        product_info = {
            "name": "Test Reusable Long", "type": "reusable",
            "manufacturing_impact": {"energy_mj": 10.0},
            "use_phase_impact": {"energy_per_use_mj": 0.1, "lifespan_uses": 100, "waste_per_use_g": 0.0},
            "end_of_life": {"weight_g": 200.0, "actual_recycle_rate_percent": 50.0}
        }
        impact = calculate_annual_impact(product_info, usage_per_day=1, days_per_year=50)
        
        self.assertEqual(impact["num_items_per_year"], 1)  # ceil(50 uses / 100 lifespan) = 1
        
        expected_mfg_energy = 1 * 10.0
        expected_use_energy = 50 * 0.1  # 50 total uses
        self.assertAlmostEqual(impact["total_annual_energy_mj"], expected_mfg_energy + expected_use_energy)
        
        expected_waste_per_item_eol = 200.0 * (1 - 0.50)  # 100g
        self.assertAlmostEqual(impact["total_annual_waste_g"], 1 * expected_waste_per_item_eol)

    def test_calculate_annual_impact_reusable_multiple_items_lifespan(self):
        """Test impact for a reusable item where multiple items are needed within a year."""
        product_info = {
            "name": "Test Reusable Short", "type": "reusable",
            "manufacturing_impact": {"energy_mj": 5.0},
            "use_phase_impact": {"energy_per_use_mj": 0.1, "lifespan_uses": 10, "waste_per_use_g": 0.0},
            "end_of_life": {"weight_g": 100.0, "actual_recycle_rate_percent": 0.0}
        }
        impact = calculate_annual_impact(product_info, usage_per_day=3, days_per_year=10)  # 30 total uses
        
        self.assertEqual(impact["num_items_per_year"], 3)  # ceil(30 uses / 10 lifespan) = 3
        
        expected_mfg_energy = 3 * 5.0
        expected_use_energy = 30 * 0.1
        self.assertAlmostEqual(impact["total_annual_energy_mj"], expected_mfg_energy + expected_use_energy)
        self.assertAlmostEqual(impact["total_annual_waste_g"], 3 * 100.0)  # 0% recycle rate

    def test_calculate_annual_impact_reusable_zero_lifespan(self):
        """Test impact for a reusable item with lifespan_uses = 0 (edge case)."""
        product_info = {
            "name": "Test Reusable Zero Life", "type": "reusable",
            "manufacturing_impact": {"energy_mj": 5.0},
            "use_phase_impact": {"energy_per_use_mj": 0.1, "lifespan_uses": 0, "waste_per_use_g": 0.0},
            "end_of_life": {"weight_g": 100.0, "actual_recycle_rate_percent": 0.0}
        }
        impact = calculate_annual_impact(product_info, usage_per_day=3, days_per_year=10)  # 30 total uses
        
        # Should be treated as lifespan 1, so 1 item per use
        self.assertEqual(impact["num_items_per_year"], 30) 
        
        expected_mfg_energy = 30 * 5.0
        expected_use_energy = 30 * 0.1
        self.assertAlmostEqual(impact["total_annual_energy_mj"], expected_mfg_energy + expected_use_energy)
        self.assertAlmostEqual(impact["total_annual_waste_g"], 30 * 100.0)

    @patch('lifecycle_planner.src.comparison_logic.get_product_data')
    def test_compare_products(self, mock_get_product_data):
        """Test the compare_products function with mocked data."""
        mock_data = {
            "test_category": [
                {
                    "name": "Prod A", "type": "disposable",
                    "manufacturing_impact": {"energy_mj": 1},
                    "use_phase_impact": {"energy_per_use_mj": 0, "lifespan_uses": 1, "waste_per_use_g": 0.0}, # Added waste_per_use_g
                    "end_of_life": {"weight_g": 10, "actual_recycle_rate_percent": 0}
                },
                {
                    "name": "Prod B", "type": "reusable",
                    "manufacturing_impact": {"energy_mj": 10},
                    "use_phase_impact": {"energy_per_use_mj": 0.1, "lifespan_uses": 100, "waste_per_use_g": 0.0}, # Added waste_per_use_g
                    "end_of_life": {"weight_g": 100, "actual_recycle_rate_percent": 0}
                }
            ]
        }
        mock_get_product_data.return_value = mock_data
        
        results = compare_products("test_category", usage_per_day=1, days_per_year=10)
        
        self.assertEqual(len(results), 2)
        
        # Product A (Disposable)
        self.assertEqual(results[0]["product_name"], "Prod A")
        self.assertEqual(results[0]["num_items_per_year"], 10) # 1 * 10 uses
        self.assertAlmostEqual(results[0]["total_annual_energy_mj"], 10 * 1) # 10 items * 1 MJ/item_mfg + 10 items * 0 MJ/item_use
        self.assertAlmostEqual(results[0]["total_annual_waste_g"], 10 * 10) # 10 items * 10g/item_eol
        
        # Product B (Reusable)
        self.assertEqual(results[1]["product_name"], "Prod B")
        self.assertEqual(results[1]["num_items_per_year"], 1) # ceil(10 uses / 100 lifespan) = 1 item
        # Energy: (1 item_mfg * 10 MJ/item_mfg) + (10 total_uses * 0.1 MJ/use)
        self.assertAlmostEqual(results[1]["total_annual_energy_mj"], (1 * 10) + (10 * 0.1))
        self.assertAlmostEqual(results[1]["total_annual_waste_g"], 1 * 100) # 1 item_eol * 100g/item_eol

    @patch('builtins.print') # To suppress "Error: Category not found" print during test
    def test_compare_products_invalid_category(self, mock_print):
        """Test compare_products with a non-existent category."""
        # Need to mock get_product_data if it's called by compare_products before returning []
        # For this test, we assume get_product_data returns valid data, but the category is not in it.
        # If get_product_data is not mocked here, it will use the actual data.
        # The current implementation of compare_products calls get_product_data()
        with patch('lifecycle_planner.src.comparison_logic.get_product_data') as mock_get_actual_data:
            mock_get_actual_data.return_value = {"coffee_containers": []} # Return some valid structure
            results = compare_products("non_existent_category", 1, 10)
            self.assertEqual(results, [])
            mock_print.assert_any_call("Error: Category 'non_existent_category' not found.")


if __name__ == '__main__':
    unittest.main()
