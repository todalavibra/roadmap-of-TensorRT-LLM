import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_bar_chart(df: pd.DataFrame, x_column: str, y_column: str, title: str = "Bar Chart", output_path: str = "bar_chart.png"):
    """
    Generates a bar chart and saves it to a file.

    Args:
        df: pandas DataFrame containing the data.
        x_column: Name of the column to use for the x-axis.
        y_column: Name of the column to use for the y-axis.
        title: Title of the chart. Defaults to "Bar Chart".
        output_path: Path to save the generated chart image. Defaults to "bar_chart.png".

    Raises:
        ValueError: If x_column or y_column are not in df.columns.
    """
    if x_column not in df.columns:
        error_msg = f"Error: x_column '{x_column}' not found in DataFrame columns: {df.columns.tolist()}"
        print(error_msg)
        raise ValueError(error_msg)
    if y_column not in df.columns:
        error_msg = f"Error: y_column '{y_column}' not found in DataFrame columns: {df.columns.tolist()}"
        print(error_msg)
        raise ValueError(error_msg)

    plt.figure()
    plt.bar(df[x_column], df[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(title)
    plt.savefig(output_path)
    plt.clf() # Clear the current figure
    plt.close() # Close the figure window

def generate_line_graph(df: pd.DataFrame, x_column: str, y_column: str, title: str = "Line Graph", output_path: str = "line_graph.png"):
    """
    Generates a line graph and saves it to a file.

    Args:
        df: pandas DataFrame containing the data.
        x_column: Name of the column to use for the x-axis.
        y_column: Name of the column to use for the y-axis.
        title: Title of the chart. Defaults to "Line Graph".
        output_path: Path to save the generated chart image. Defaults to "line_graph.png".

    Raises:
        ValueError: If x_column or y_column are not in df.columns.
    """
    if x_column not in df.columns:
        error_msg = f"Error: x_column '{x_column}' not found in DataFrame columns: {df.columns.tolist()}"
        print(error_msg)
        raise ValueError(error_msg)
    if y_column not in df.columns:
        error_msg = f"Error: y_column '{y_column}' not found in DataFrame columns: {df.columns.tolist()}"
        print(error_msg)
        raise ValueError(error_msg)

    plt.figure()
    plt.plot(df[x_column], df[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(title)
    plt.savefig(output_path)
    plt.clf() # Clear the current figure
    plt.close() # Close the figure window

def generate_scatter_plot(df: pd.DataFrame, x_column: str, y_column: str, title: str = "Scatter Plot", output_path: str = "scatter_plot.png"):
    """
    Generates a scatter plot and saves it to a file.

    Args:
        df: pandas DataFrame containing the data.
        x_column: Name of the column to use for the x-axis.
        y_column: Name of the column to use for the y-axis.
        title: Title of the chart. Defaults to "Scatter Plot".
        output_path: Path to save the generated chart image. Defaults to "scatter_plot.png".

    Raises:
        ValueError: If x_column or y_column are not in df.columns.
    """
    if x_column not in df.columns:
        error_msg = f"Error: x_column '{x_column}' not found in DataFrame columns: {df.columns.tolist()}"
        print(error_msg)
        raise ValueError(error_msg)
    if y_column not in df.columns:
        error_msg = f"Error: y_column '{y_column}' not found in DataFrame columns: {df.columns.tolist()}"
        print(error_msg)
        raise ValueError(error_msg)

    plt.figure()
    plt.scatter(df[x_column], df[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(title)
    plt.savefig(output_path)
    plt.clf() # Clear the current figure
    plt.close() # Close the figure window
