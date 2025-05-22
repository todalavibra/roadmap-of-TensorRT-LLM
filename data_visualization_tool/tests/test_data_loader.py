import unittest
import pandas as pd
import os

# Adjust import path for data_loader based on execution context
try:
    from data_visualization_tool.src.data_loader import load_csv
except ImportError:
    # This path might be needed if tests are run from the root project directory
    # and the 'data_visualization_tool' directory itself is not directly on PYTHONPATH
    # or when the module structure is interpreted differently by the test runner.
    import sys
    # Assuming the script is run from a context where 'data_visualization_tool' is a subdir
    # or the structure is data_visualization_tool/src and data_visualization_tool/tests
    # We need to add the 'src' directory to the path or ensure the parent of 'data_visualization_tool' is.
    # For simplicity, if 'data_visualization_tool/src' is not directly importable,
    # let's assume 'src' needs to be added to sys.path relative to this test file's location.
    # This is a common way to handle local package imports in tests.
    
    # Correct path adjustment: Add the directory *containing* 'data_visualization_tool' to sys.path
    # so that `from data_visualization_tool.src...` works.
    # Or, add `data_visualization_tool/src` to sys.path to directly import `data_loader`.
    
    # Let's try a more robust way to find the 'src' directory
    current_dir = os.path.dirname(os.path.abspath(__file__)) # data_visualization_tool/tests
    project_root = os.path.dirname(current_dir) # data_visualization_tool
    src_path = os.path.join(project_root, 'src') # data_visualization_tool/src
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # If the above doesn't work because the tests are run from a directory
    # such that 'data_visualization_tool' itself is the top-level package visible,
    # then the original `from data_visualization_tool.src.data_loader import load_csv` should work.
    # The issue often arises when `python -m unittest discover` is run from the project root.
    # Let's try adding the project root to sys.path if 'data_visualization_tool.src' is not found
    # This allows Python to see 'data_visualization_tool' as a package.
    # This logic is getting complex. A simpler way for tests is often to set PYTHONPATH externally,
    # or to structure the project such that `src` is directly importable.
    # For now, let's assume the test runner or PYTHONPATH is set up correctly
    # and the primary import error is due to not finding 'data_visualization_tool.src' directly.
    
    # Re-attempting a common structure for running tests with `python -m unittest discover`
    # from the directory containing `data_visualization_tool`
    # In this case, `data_visualization_tool` is a package.
    
    # If the first try fails, it means 'data_visualization_tool' is not seen as a package.
    # Let's assume we are in data_visualization_tool/tests
    # and we need to import from data_visualization_tool/src
    
    # Assuming this test file is in data_visualization_tool/tests/
    # and src is data_visualization_tool/src/
    # We need to make 'data_visualization_tool' the package root for imports.
    # This can be achieved by adding the parent of 'data_visualization_tool' to sys.path
    # or more simply, by ensuring tests are run with the correct working directory.
    
    # Let's try a simpler approach for sys.path modification for typical project structures:
    # Add the parent directory of 'data_visualization_tool' to sys.path
    # This test file is 'data_visualization_tool/tests/test_data_loader.py'
    # os.path.dirname(__file__) -> 'data_visualization_tool/tests'
    # os.path.dirname(os.path.dirname(__file__)) -> 'data_visualization_tool' (this is our project root)
    # We want the directory *containing* 'data_visualization_tool' if we are to treat 'data_visualization_tool' as a package.
    # Or, more simply, add the 'src' directory directly if we treat 'src' files as top-level modules.
    
    # Let's adjust to a common way unittest discovery works:
    # If you run `python -m unittest discover data_visualization_tool/tests` from the project root,
    # the project root (containing `data_visualization_tool` directory) is added to sys.path.
    # So, `from data_visualization_tool.src.data_loader import load_csv` should work.
    
    # The problem might be if `data_visualization_tool` itself is the root.
    # Let's assume the structure is /app (root for execution)
    # /app/data_visualization_tool/src/data_loader.py
    # /app/data_visualization_tool/tests/test_data_loader.py
    # If running from /app, then `from data_visualization_tool.src.data_loader import load_csv` is correct.
    
    # The provided solution uses relative imports like `.data_loader` in main.py
    # For tests, it's usually better to use absolute imports from the project root.
    
    # Final attempt at robustly finding src:
    # This file: data_visualization_tool/tests/test_data_loader.py
    # We want to import: data_visualization_tool/src/data_loader.py
    # Add project root to sys.path
    project_root_for_imports = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    # This goes up two levels: tests -> data_visualization_tool -> parent of data_visualization_tool
    # This is correct if the CWD for the test runner is *inside* data_visualization_tool
    # Let's assume the CWD is the root of the repo, which contains 'data_visualization_tool'
    # Then 'data_visualization_tool' is already effectively a package.
    
    # Let's stick to the original import and assume the environment (PYTHONPATH or test runner CWD) is correct.
    # The `except ImportError` is a fallback.
    # A common simple fix is to add `src` to path if `main.py` is in `src`
    # current_script_path = os.path.dirname(os.path.abspath(__file__))
    # project_src_path = os.path.join(os.path.dirname(current_script_path), "src")
    # if project_src_path not in sys.path:
    #    sys.path.insert(0, project_src_path)
    # from data_loader import load_csv # This would now work if src is in path.

    # Given the main.py uses `from .data_loader import load_csv`, it implies `src` is a package.
    # So tests should probably import from `data_visualization_tool.src.data_loader`
    # If that fails, it's an environment issue. The code below is a common workaround.
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
    from data_loader import load_csv


# Define paths relative to this test file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "sample_data")
VALID_DATA_PATH = os.path.join(SAMPLE_DATA_DIR, "valid_data.csv")
EMPTY_DATA_PATH = os.path.join(SAMPLE_DATA_DIR, "empty_data.csv")
MALFORMED_DATA_PATH = os.path.join(SAMPLE_DATA_DIR, "malformed_data.csv")
NON_EXISTENT_FILE_PATH = os.path.join(SAMPLE_DATA_DIR, "non_existent_file.csv")

class TestDataLoader(unittest.TestCase):

    def test_load_csv_valid_file(self):
        """Test loading a valid CSV file."""
        df = load_csv(VALID_DATA_PATH)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (4, 4)) # 4 rows, 4 columns
        self.assertEqual(df['name'][0], 'A')
        self.assertEqual(df['value1'][1], 15)

    def test_load_csv_non_existent_file(self):
        """Test loading a non-existent CSV file."""
        with self.assertRaises(FileNotFoundError):
            load_csv(NON_EXISTENT_FILE_PATH)

    def test_load_csv_empty_file(self):
        """Test loading an empty CSV file."""
        with self.assertRaises(pd.errors.EmptyDataError):
            load_csv(EMPTY_DATA_PATH)

    def test_load_csv_malformed_file(self):
        """Test loading a malformed CSV file."""
        # Depending on the pandas version and the exact nature of malformation,
        # this could also raise other errors like CParserError.
        # ParserError is a more general one.
        with self.assertRaises(pd.errors.ParserError):
            load_csv(MALFORMED_DATA_PATH)

if __name__ == '__main__':
    unittest.main()
