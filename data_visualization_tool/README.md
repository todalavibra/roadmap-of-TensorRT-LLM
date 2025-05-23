# Data Visualization Tool

## Description
This tool allows users to generate simple bar charts, line graphs, and scatter plots from data in CSV files. It provides a command-line interface for easy generation and customization of plots.

## Features
*   Load data from CSV files.
*   Generate Bar Charts.
*   Generate Line Graphs.
*   Generate Scatter Plots.
*   Command-line interface for ease of use.
*   Customizable plot titles and output file names.
*   Error handling for common issues like missing files or incorrect column names.

## Prerequisites
*   Python 3 (e.g., Python 3.7+ recommended)
*   pip (Python package installer)

## Installation
1.  **Clone the repository (optional):**
    If you have downloaded the source as a ZIP, extract it. Otherwise, you can clone it using git:
    ```bash
    git clone <repository_url> 
    # Replace <repository_url> with the actual URL of the repository
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd data_visualization_tool
    ```
3.  **Install dependencies:**
    This will install pandas, matplotlib, and seaborn.
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To use the tool, run the `main.py` script from the `src` directory. You can also run it as a module from the project root.

**Syntax:**
```bash
python src/main.py file_path plot_type x_column y_column [OPTIONS]
```
or from the project root:
```bash
python -m data_visualization_tool.src.main file_path plot_type x_column y_column [OPTIONS]
```

**Command-Line Arguments:**

*   `file_path`: (Required) Path to the input CSV file.
*   `plot_type`: (Required) Type of plot to generate.
    *   Choices: `bar`, `line`, `scatter`.
*   `x_column`: (Required) Name of the column from the CSV file to be used for the X-axis.
*   `y_column`: (Required) Name of the column from the CSV file to be used for the Y-axis.
*   `--title TITLE`: (Optional) Title for the plot. If not provided, a default title will be generated (e.g., "Bar chart for x_column vs y_column").
*   `--output_path OUTPUT_PATH`: (Optional) File path to save the generated plot image. If not provided, a default name like `{plot_type}_chart.png` (e.g., `bar_chart.png`) will be used in the current working directory.

**Examples:**

1.  Generate a bar chart with default title and output path, assuming `data.csv` is in a `sample_data` directory:
    ```bash
    python src/main.py sample_data/data.csv bar category_column value_column
    ```
    *(Note: Replace `sample_data/data.csv`, `category_column`, and `value_column` with your actual file path and column names.)*

2.  Generate a line graph with a custom title and output file name:
    ```bash
    python src/main.py path/to/your_sales_data.csv line month sales --title "Monthly Sales Trend" --output_path reports/sales_trend.png
    ```
    *(Ensure the `reports` directory exists or adjust the path.)*

3.  Generate a scatter plot for `feature_A` vs `feature_B` from `dataset.csv`:
    ```bash
    python src/main.py dataset.csv scatter feature_A feature_B --title "Feature A vs Feature B"
    ```

## Input CSV Format
The input CSV file should contain a header row as its first line. The column names specified for the X-axis (`x_column`) and Y-axis (`y_column`) must be present in this header row.

Example:
```csv
date,temperature,humidity
2024-01-01,10,60
2024-01-02,12,65
...
```

## Running Tests
To run the unit tests for the tool, navigate to the project's root directory (`data_visualization_tool`) and execute the following command:
```bash
python -m unittest discover data_visualization_tool/tests
```
Alternatively, if your current working directory is `data_visualization_tool`, you might be able to use:
```bash
python -m unittest discover tests
```
The tests ensure that data loading and plotting functionalities work as expected. Sample data for tests is located in `data_visualization_tool/tests/sample_data/`. Generated plots during tests are saved in `data_visualization_tool/tests/test_outputs/` and cleaned up afterwards.
