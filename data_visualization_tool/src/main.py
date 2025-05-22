#!/usr/bin/env python3
import argparse
import sys
import pandas as pd # Import pandas for specific exceptions

try:
    from .data_loader import load_csv
    from .plotter import generate_bar_chart, generate_line_graph, generate_scatter_plot
except ImportError:
    # Fallback for direct execution if modules are not found in the current package.
    # This can happen if the script is run as "python src/main.py" from the project root.
    from data_loader import load_csv
    from plotter import generate_bar_chart, generate_line_graph, generate_scatter_plot


def main():
    parser = argparse.ArgumentParser(description="Data Visualization Tool")
    parser.add_argument("file_path", type=str, help="Path to the CSV file.")
    parser.add_argument("plot_type", type=str, choices=["bar", "line", "scatter"],
                        help="Type of plot to generate (bar, line, scatter).")
    parser.add_argument("x_column", type=str, help="Name of the column for the x-axis.")
    parser.add_argument("y_column", type=str, help="Name of the column for the y-axis.")
    parser.add_argument("--title", type=str, default=None, help="Optional title for the plot.")
    parser.add_argument("--output_path", type=str, default=None,
                        help="Optional path to save the plot image.")

    args = parser.parse_args()

    try:
        print(f"Loading data from {args.file_path}...")
        df = load_csv(args.file_path)
    except FileNotFoundError:
        # Error message is printed by load_csv
        sys.exit(1)
    except pd.errors.EmptyDataError:
        # Error message is printed by load_csv
        sys.exit(1)
    except pd.errors.ParserError:
        # Error message is printed by load_csv
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while loading the data: {e}")
        sys.exit(1)

    if df is None: # Should be caught by specific exceptions, but as a safeguard
        print("Failed to load data. Exiting.")
        sys.exit(1)

    # Determine output_path
    actual_output_path = args.output_path
    if actual_output_path is None:
        actual_output_path = f"{args.plot_type}_chart.png"

    # Determine title
    actual_title = args.title
    if actual_title is None:
        actual_title = f"{args.plot_type.capitalize()} chart for {args.x_column} vs {args.y_column}"

    print(f"Generating {args.plot_type} plot...")

    try:
        if args.plot_type == "bar":
            generate_bar_chart(df, args.x_column, args.y_column, title=actual_title, output_path=actual_output_path)
        elif args.plot_type == "line":
            generate_line_graph(df, args.x_column, args.y_column, title=actual_title, output_path=actual_output_path)
        elif args.plot_type == "scatter":
            generate_scatter_plot(df, args.x_column, args.y_column, title=actual_title, output_path=actual_output_path)
        else:
            # This case should ideally not be reached due to argparse choices
            print(f"Error: Invalid plot_type '{args.plot_type}'. Please choose from 'bar', 'line', or 'scatter'.")
            sys.exit(1)
        
        print(f"Plot saved to {actual_output_path}.")

    except ValueError as ve:
        # Error message is printed by plotting functions
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while generating the plot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
