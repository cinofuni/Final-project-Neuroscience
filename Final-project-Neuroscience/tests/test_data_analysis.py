import pandas as pd
import sys
import os
# Add the src directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.data_analysis import count_by_range
from src.data_analysis import analyze_column_significant_only




# Test function
def test_count_by_range():
    # Create a sample DataFrame
    data = {
        'col1': [3, 2, 1, 3, 2],
        'col2': [2, 2, 1, 3, 4],
        'col3': [4, 2, 1, 2, 3],
        'col4': [1, 3, 2, 3, 4],
        'col5': [2, 1, 2, 3, 1],
        'letter_col': ['A', 'B', 'A', 'A', 'B']
    }
    df = pd.DataFrame(data)
    
    # Call the function
    result = count_by_range(df, ['col1', 'col2', 'col3', 'col4', 'col5'], 'letter_col', 2, 4)

    # Expected result
    expected_result = pd.DataFrame({
        'Count': [2, 2],
        'Percentage': [66.66666666666666, 100.000000]
    }, index=['A', 'B'])

    # Simple check
    if result.equals(expected_result):
        print("Test Passed!")
    else:
        print("Test Failed!")
        print("Expected:")
        print(expected_result)
        print("Got:")
        print(result)

# Run the test
test_count_by_range()




# Test function for analyze_column_significant_only
def test_analyze_column_significant_only():
    # Sample DataFrame for testing
    good_data = pd.DataFrame({
        'Count': [5, 15, 8, 12],
    }, index=['A', 'B', 'C', 'D'])

    bad_data = pd.DataFrame({
        'Count': [10, 20, 8, 2],
    }, index=['A', 'B', 'C', 'D'])

    # Column to analyze
    column = 'Test Column'

    # Run the function
    results = analyze_column_significant_only(good_data, bad_data, column)

    # Check if we got any significant result
    if len(results) == 1:
        print("Test passed.")
    else:
        print("Test failed.")

# Run the test
test_analyze_column_significant_only()
