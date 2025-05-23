# Comparative Product Lifecycle Analyzer (Phase 1)

## Description
This is a command-line interface (CLI) tool designed to help users compare the estimated lifecycle environmental impacts (specifically waste generation and energy consumption) of common product choices. This is Phase 1 of the project, meaning it currently features a limited set of products and uses simplified data for its calculations.

## Purpose/Goal
The primary goal of this tool is to foster more informed decision-making by providing illustrative comparisons of product lifecycles. It aims to raise awareness about the potential environmental consequences associated with everyday choices. 

**Important Note:** This tool is intended for estimation and educational awareness. It is **not** a substitute for precise, scientific Life Cycle Assessment (LCA) studies.

## Current Scope & Features (Phase 1)
*   **Product Categories Analyzed:**
    *   `coffee_containers`
    *   `shopping_bags`
    *   `water_bottles`
*   **Interface:** Command-Line Interface (CLI).
*   **Calculations:** Estimates annual waste generation (in grams/kilograms) and energy consumption (in Megajoules - MJ) based on user-provided usage patterns.

## Prerequisites
*   Python 3 (Python 3.7 or newer is recommended).

## How to Run
1.  **Navigate to the project directory:**
    Open your terminal or command prompt and change to the main project directory:
    ```bash
    cd lifecycle_planner
    ```
2.  **Execute the script:**
    Run the `main.py` script from the `src` directory, providing the required arguments:
    ```bash
    python src/main.py [CATEGORY] [USAGE_PER_DAY] --days_per_year [DAYS]
    ```
    (Depending on your system configuration, you might need to use `python3 src/main.py`.)

    **Arguments:**
    *   `CATEGORY`: The category of products you want to compare. Your choices are:
        *   `coffee_containers`
        *   `shopping_bags`
        *   `water_bottles`
    *   `USAGE_PER_DAY`: An integer representing your daily usage for this product category (e.g., `2` if you use two coffee containers per day).
    *   `--days_per_year DAYS` (or `-d DAYS`): An optional integer specifying the number of days in a year for which the calculation should be made. Defaults to `365` if not provided.

    **Examples:**
    ```bash
    # Compare coffee containers assuming 2 uses per day for a full year
    python src/main.py coffee_containers 2

    # Compare shopping bags assuming 3 uses per day over 300 days
    python src/main.py shopping_bags 3 --days_per_year 300

    # Compare water bottles assuming 1 use per day for 200 days
    python src/main.py water_bottles 1 -d 200
    ```

## Understanding the Output
The tool provides the following information for each product within the chosen category:
*   **Items needed per year:** The estimated number of individual items of that type you would consume annually.
*   **Total Annual Energy:** The total estimated energy consumed over the year, in Megajoules (MJ). This includes both manufacturing energy and energy used during the use phase (e.g., washing).
*   **Total Annual Waste:** The total estimated waste generated over the year, shown in grams (g) and kilograms (kg). This is the weight of items that are disposed of and not successfully recycled.
*   **Details:** A breakdown of:
    *   **Manufacturing Energy:** Energy used to produce the items needed annually.
    *   **Use Phase Energy:** Energy consumed during the use of the products (e.g., washing reusable items).

## Data: Assumptions and Simplifications (CRUCIAL)
**The lifecycle data used in this tool is based on approximations, averages, and publicly available estimates. It is intended for illustrative and educational purposes only and is not a substitute for rigorous scientific Life Cycle Assessment (LCA).**

Real LCA data is highly complex and varies significantly based on numerous factors, including specific manufacturing processes, geographical location of production and use, user behavior (e.g., washing habits), and actual end-of-life management practices in different regions. The figures presented in this tool involve necessary simplifications for this phase of development.

Key simplifications include:
*   Transportation impacts (e.g., shipping products from factory to consumer) are generally not included.
*   Raw material extraction details and their full environmental loads are abstracted.
*   End-of-life scenarios (e.g., landfill vs. incineration vs. recycling pathways) are generalized.
*   Manufacturing energy figures are rough estimates.
*   "Recyclable locally" is a general assumption and actual local capabilities can vary widely.
*   "Actual recycle rate percent" is an estimated average and can differ significantly based on region and material type.

Data sources for placeholders and estimates include general environmental science reports, educational websites, and publicly available articles. Specific, traceable citations for each individual data point are not provided in this phase of the project.

## Running Tests (For Developers/Contributors)
To run the unit tests for the tool, navigate to the project's root directory (`lifecycle_planner`) and execute the following command:
```bash
python -m unittest discover lifecycle_planner/tests
```
This will automatically find and run all tests in the `tests` directory.

## Future Development (Optional)
*   Expand the product database with more categories and items.
*   Develop a simple web interface for easier use.
*   Allow users to customize more lifecycle parameters.
*   Integrate more detailed and region-specific data where feasible.
