import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Loads a CSV file into a pandas DataFrame.

    Args:
        file_path: The path to the CSV file.

    Returns:
        A pandas DataFrame containing the data from the CSV file.

    Raises:
        FileNotFoundError: If the CSV file is not found at the specified path.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If an error occurs while parsing the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        raise
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty.")
        raise
    except pd.errors.ParserError:
        print(f"Error: An error occurred while parsing the file '{file_path}'.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
