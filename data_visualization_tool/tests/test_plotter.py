import unittest
from unittest.mock import patch, call
import pandas as pd
import os
import sys

# Adjust import path for plotter based on execution context
try:
    from data_visualization_tool.src.plotter import generate_bar_chart, generate_line_graph, generate_scatter_plot
except ImportError:
    # Assuming this test file is in data_visualization_tool/tests/
    # and src is data_visualization_tool/src/
    # Add the 'src' directory to sys.path for direct import of plotter
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
    from plotter import generate_bar_chart, generate_line_graph, generate_scatter_plot

class TestPlotter(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.sample_df = pd.DataFrame({
            'category': ['X', 'Y', 'Z'],
            'value': [10, 20, 30],
            'time': [1, 2, 3]  # Added for line/scatter if needed
        })
        self.test_output_files = []
        # Ensure the directory for test outputs exists if needed, or clean up specific files
        self.output_dir = os.path.join(os.path.dirname(__file__), "test_outputs")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def tearDown(self):
        """Tear down after test methods."""
        for f_path in self.test_output_files:
            try:
                os.remove(f_path)
            except FileNotFoundError:
                pass # File was not created, which might be part of a test
        # Clean up the output directory if it's empty and was created by tests
        if os.path.exists(self.output_dir) and not os.listdir(self.output_dir):
            os.rmdir(self.output_dir)


    # --- Tests for generate_bar_chart ---
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.bar')
    @patch('matplotlib.pyplot.figure') # Patch figure to avoid showing plots
    @patch('matplotlib.pyplot.clf')
    @patch('matplotlib.pyplot.close')
    def test_generate_bar_chart_valid_input(self, mock_close, mock_clf, mock_figure, mock_bar, mock_ylabel, mock_xlabel, mock_title, mock_savefig):
        """Test generate_bar_chart with valid inputs."""
        output_path = os.path.join(self.output_dir, "test_bar_chart.png")
        self.test_output_files.append(output_path)
        
        generate_bar_chart(self.sample_df, 'category', 'value', title="Test Bar", output_path=output_path)
        
        mock_figure.assert_called_once()
        mock_bar.assert_called_once()
        # Check that df['category'] and df['value'] were accessed
        pd.testing.assert_series_equal(mock_bar.call_args[0][0], self.sample_df['category'])
        pd.testing.assert_series_equal(mock_bar.call_args[0][1], self.sample_df['value'])
        
        mock_xlabel.assert_called_once_with('category')
        mock_ylabel.assert_called_once_with('value')
        mock_title.assert_called_once_with("Test Bar")
        mock_savefig.assert_called_once_with(output_path)
        mock_clf.assert_called_once()
        mock_close.assert_called_once()

    def test_generate_bar_chart_invalid_x_column(self):
        """Test generate_bar_chart with an invalid x_column."""
        with self.assertRaises(ValueError):
            generate_bar_chart(self.sample_df, 'invalid_col', 'value')

    def test_generate_bar_chart_invalid_y_column(self):
        """Test generate_bar_chart with an invalid y_column."""
        with self.assertRaises(ValueError):
            generate_bar_chart(self.sample_df, 'category', 'invalid_col')

    # --- Tests for generate_line_graph ---
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.plot')
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.clf')
    @patch('matplotlib.pyplot.close')
    def test_generate_line_graph_valid_input(self, mock_close, mock_clf, mock_figure, mock_plot, mock_ylabel, mock_xlabel, mock_title, mock_savefig):
        """Test generate_line_graph with valid inputs."""
        output_path = os.path.join(self.output_dir, "test_line_graph.png")
        self.test_output_files.append(output_path)

        generate_line_graph(self.sample_df, 'time', 'value', title="Test Line", output_path=output_path)
        
        mock_figure.assert_called_once()
        mock_plot.assert_called_once()
        pd.testing.assert_series_equal(mock_plot.call_args[0][0], self.sample_df['time'])
        pd.testing.assert_series_equal(mock_plot.call_args[0][1], self.sample_df['value'])
        
        mock_xlabel.assert_called_once_with('time')
        mock_ylabel.assert_called_once_with('value')
        mock_title.assert_called_once_with("Test Line")
        mock_savefig.assert_called_once_with(output_path)
        mock_clf.assert_called_once()
        mock_close.assert_called_once()

    def test_generate_line_graph_invalid_x_column(self):
        """Test generate_line_graph with an invalid x_column."""
        with self.assertRaises(ValueError):
            generate_line_graph(self.sample_df, 'invalid_col', 'value')

    def test_generate_line_graph_invalid_y_column(self):
        """Test generate_line_graph with an invalid y_column."""
        with self.assertRaises(ValueError):
            generate_line_graph(self.sample_df, 'time', 'invalid_col')

    # --- Tests for generate_scatter_plot ---
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.scatter')
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.clf')
    @patch('matplotlib.pyplot.close')
    def test_generate_scatter_plot_valid_input(self, mock_close, mock_clf, mock_figure, mock_scatter, mock_ylabel, mock_xlabel, mock_title, mock_savefig):
        """Test generate_scatter_plot with valid inputs."""
        output_path = os.path.join(self.output_dir, "test_scatter_plot.png")
        self.test_output_files.append(output_path)

        generate_scatter_plot(self.sample_df, 'time', 'value', title="Test Scatter", output_path=output_path)
        
        mock_figure.assert_called_once()
        mock_scatter.assert_called_once()
        pd.testing.assert_series_equal(mock_scatter.call_args[0][0], self.sample_df['time'])
        pd.testing.assert_series_equal(mock_scatter.call_args[0][1], self.sample_df['value'])
        
        mock_xlabel.assert_called_once_with('time')
        mock_ylabel.assert_called_once_with('value')
        mock_title.assert_called_once_with("Test Scatter")
        mock_savefig.assert_called_once_with(output_path)
        mock_clf.assert_called_once()
        mock_close.assert_called_once()

    def test_generate_scatter_plot_invalid_x_column(self):
        """Test generate_scatter_plot with an invalid x_column."""
        with self.assertRaises(ValueError):
            generate_scatter_plot(self.sample_df, 'invalid_col', 'value')

    def test_generate_scatter_plot_invalid_y_column(self):
        """Test generate_scatter_plot with an invalid y_column."""
        with self.assertRaises(ValueError):
            generate_scatter_plot(self.sample_df, 'time', 'invalid_col')

if __name__ == '__main__':
    # This allows running the tests directly from this file
    # For discovery, use `python -m unittest discover data_visualization_tool/tests`
    # from the project root.
    # To make imports work when running this file directly, ensure 'src' is in PYTHONPATH
    # or use the sys.path manipulation as done at the top of the file.
    unittest.main()
