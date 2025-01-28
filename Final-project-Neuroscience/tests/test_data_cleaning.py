import numpy as np
import pandas as pd
from src.data_cleaning import lobe_extraction
from src.data_cleaning import clean_lobe_column
from src.data_cleaning import remove_rows_with_too_many_nans
from src.data_cleaning import refill_nan_with_previous
from src.data_cleaning import filter_rows_by_conditions
from src.data_cleaning import calculate_mean_age



'''First test:'''
def test_lobe_extraction():
    # Sample input DataFrame
    data = {"Op_Type": ["T Lx", "FOP", "O Lx", "P", None]}
    df = pd.DataFrame(data)
    
    # Expected output for the 'lobe' column
    expected_lobe = ["T", "F", "O", "P", None]
    
    # Run the function
    result_df = lobe_extraction(df, "Op_Type")
    
    # Assertion: Check if the 'lobe' column matches the expected output
    assert list(result_df["lobe"]) == expected_lobe, "Test failed: lobe extraction is incorrect."

# Run the test
test_lobe_extraction()
print("Test passed!")


'''Second test'''
def test_clean_lobe_column():
    # Sample input DataFrame
    data = {
        "lobe": ["T", "F", "X", None, "P", "O", "TF", ""],
        "other_column": [1, 2, 3, 4, 5, 6, 7, 8],  # Extra column to ensure it's preserved
    }
    df = pd.DataFrame(data)
    
    # Expected output: Only rows where 'lobe' is "T", "F", "P", or "O"
    expected_lobe = ["T", "F", "P", "O"]
    
    # Run the function
    result_df = clean_lobe_column(df)
    
    # Assertion: Check if the 'lobe' column in the cleaned DataFrame matches the expected values
    assert list(result_df["lobe"]) == expected_lobe, "Test failed: Cleaned lobe column is incorrect."

# Run the test
test_clean_lobe_column()
print("Test passed!")



def test_remove_rows_with_too_many_nans():
    # Sample input DataFrame
    data = {
        "col1": [1, None, 3, None, 5],
        "col2": [None, None, 3, 4, None],
        "col3": [1, 2, None, None, None],
        "other_col": [10, 20, 30, 40, 50],  # Extra column to ensure it's preserved
    }
    df = pd.DataFrame(data)
    
    # Specify columns to check and the maximum allowed NaNs
    columns_to_check = ["col1", "col2", "col3"]
    max_allowed_nans = 1  # Only allow at most 1 NaN in the specified columns
    
    # Expected DataFrame: Rows with more than 1 NaN in the specified columns are removed
    expected_data = {
        "col1": [1, 3],
        "col2": [None, 3],
        "col3": [1, None],
        "other_col": [10, 30],
    }
    expected_df = pd.DataFrame(expected_data)
    
    # Run the function
    result_df = remove_rows_with_too_many_nans(df, columns_to_check, max_allowed_nans)
    
    # Assertion: Check if the resulting DataFrame matches the expected DataFrame
    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False, check_exact=False)

# Run the test
test_remove_rows_with_too_many_nans()
print("Test passed!")




def test_refill_nan_with_previous():
    # Input DataFrame
    data = {
        "col1": [1.0, None, 3.0, 4.0],
        "col2": [None, 2, None, 4.0],
        "col3": [1.0, 2.0, None, None],
    }
    df = pd.DataFrame(data)
    
    # Columns to process
    columns = ["col1", "col2", "col3"]
    
    # Expected DataFrame (explicitly set dtype to float)
    expected_data = {
        "col1": [1.0, None, 3.0, 4.0],       # No changes in the first column
        "col2": [1.0, 2.0, 3.0, 4.0],    # NaN in col2 replaced by col1 values
        "col3": [1.0, 2.0, 3.0, 4.0],          # No NaNs, values remain unchanged
    }
    expected_df = pd.DataFrame(expected_data, dtype=float)  # Explicitly set dtype to float
    
    # Run the function
    result_df = refill_nan_with_previous(df, columns)
    
    # Assertion
    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=True)

# Run the test
test_refill_nan_with_previous()
print("Test passed!")



def test_filter_rows_by_conditions():
    # Sample DataFrame
    data = {
        "ILAE_Year1": [1, 3, 2, 4, 5],
        "ILAE_Year2": [2, 3, 1, 5, 4],
        "ILAE_Year3": [1, 2, 3, 4, 5],
        "ILAE_Year4": [2, 3, 4, 5, 1],
        "ILAE_Year5": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data)

    # Define conditions: 4 values in (1, 2) or (3, 5)
    conditions = [((1, 2), 4), ((3, 5), 4)]

    # Call the function
    included_df, excluded_df = filter_rows_by_conditions(
        df, ["ILAE_Year1", "ILAE_Year2", "ILAE_Year3", "ILAE_Year4", "ILAE_Year5"], conditions
    )

    # Expected results
    expected_included = pd.DataFrame({
        "ILAE_Year1": [1, 4, 5],
        "ILAE_Year2": [2, 5, 4],
        "ILAE_Year3": [1, 4, 5],
        "ILAE_Year4": [2, 5 ,1],
        "ILAE_Year5": [1, 4, 5],
    }).reset_index(drop=True)

    expected_excluded = pd.DataFrame({
        "ILAE_Year1": [3, 2],
        "ILAE_Year2": [3, 1],
        "ILAE_Year3": [2, 3],
        "ILAE_Year4": [3, 4],
        "ILAE_Year5": [2, 3],
    }).reset_index(drop=True)

    # Check results
    try:
        pd.testing.assert_frame_equal(included_df, expected_included)
        pd.testing.assert_frame_equal(excluded_df, expected_excluded)
        print("Test passed! ")
    except AssertionError as e:
        print("Test failed! ")
        print(e)

# Run the test
test_filter_rows_by_conditions()




def test_calculate_mean_age():
    # Create a test DataFrame
    test_data = {
        "age_range": [
            "1 to 5",
            "10 to 20",
            "Less than 1",
            "Over 40",
            "1.5 to 4.0",
            np.nan,  # NaN value
        ]
    }
    df = pd.DataFrame(test_data)
    
    # Expected output
    expected_data = {
        "age_range": [
            "1 to 5",
            "10 to 20",
            "Less than 1",
            "Over 40",
            "1.5 to 4.0",
            np.nan,
        ],
        "mean_age": [
            3.0,  # (1 + 5) / 2
            15.0,  # (10 + 20) / 2
            1.0,  # "Less than 1"
            40.0,  # "Over 40"
            2.75, # (1.5 + 4) / 2
            np.nan,  # NaN remains NaN
        ]
    }
    expected_df = pd.DataFrame(expected_data)
    
    # Run the function
    result_df = calculate_mean_age(df, "age_range", "mean_age")
    
    # Assert the result matches the expected output
    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)
    print("Test passed!")

# Run the test
test_calculate_mean_age()

