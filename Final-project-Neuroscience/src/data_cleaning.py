import pandas as pd
import numpy as np

'''instaling the excel file'''
df = pd.read_csv("C:/Users/Shimon Funaro/Downloads/Metadata_Release_Anon (1).csv")


'''Op_type Cleaning '''

#creating a new colunm with the lobe the patient had an operation on
def lobe_extraction(df,column):
    #creating a new column naming it 'lobe', extracting from the 'column' (Op_Type) only the "TFOP" string to the new column. 
        #making sure that it adds to the 'lobe' column specificly waht we asked for
    df["lobe"] = df[column].str.extract(r"(T|F|O|P|)", expand = False) 
    return df


def clean_lobe_column(df): 
    # Define a regular expression pattern to match rows with exactly one of the letters T, F, P, O
    valid_pattern = r'^[TFPO]$'
    
    # Filter the DataFrame based on the pattern
    cleaned_data = df[df['lobe'].str.match(valid_pattern, na=False)] #
    
    return cleaned_data



''' Post OP Cleaning '''



def remove_rows_with_too_many_nans(df, columns, max_allowed_nans):
    # Count the number of NaNs in the specified columns for each row
    nan_counts = df[columns].isna().sum(axis=1)
    print("NaN counts per row:", nan_counts)  # Debugging line
    
    # Filter rows where the NaN count exceeds the allowed maximum
    cleaned_df = df.loc[nan_counts <= max_allowed_nans].reset_index(drop=True)  # Reset index
    
    return cleaned_df

''''''

def refill_nan_with_previous(df, columns):
    for index, row in df.iterrows():
        for col_idx, col_name in enumerate(columns):
            if pd.isna(row[col_name]):  # Check if current cell is NaN
                if col_idx > 0:  # Make sure there's a previous column
                    previous_col = columns[col_idx - 1]
                    df.at[index, col_name] = row[previous_col]
    return df

def filter_rows_by_conditions(df, number_columns, conditions):
    # Track indices of rows that meet the conditions
    included_indices = set()

    for value_range, min_count in conditions:
        # Define the condition
        condition = df[number_columns].apply(
            lambda row: ((row >= value_range[0]) & (row <= value_range[1])).sum(), axis=1
        ) >= min_count

        # Add indices of rows that meet the condition
        included_indices.update(df[condition].index)

    # Create DataFrame of included rows
    included_df = df.loc[list(included_indices)].reset_index(drop=True)  # Changed to square brackets and convert to list

    # Create DataFrame of excluded rows (those not in the included indices)
    excluded_df = df.drop(index=list(included_indices)).reset_index(drop=True)

    return included_df, excluded_df


''' Ages Cleaning '''



def calculate_mean_age(df, column_name, new_column_name):

    # Initialize an empty list to store the mean values
    mean_ages = []

    # Iterate through each value in the specified column
    for value in df[column_name]:
        if pd.isna(value):
            mean_ages.append(np.nan)  # Handle NaN values
        elif value == 'Less than 1':
            mean_ages.append(1)  # Special case
        elif value == 'Over 40':
            mean_ages.append(40)  # Special case
        else:
            try:
                # Split the range and calculate the mean
                parts = value.split(' to ')
                mean_ages.append((float(parts[0]) + float(parts[1])) / 2)
            except Exception as e:
                raise ValueError(f"Invalid value '{value}' encountered in column '{column_name}': {e}")

    # Add the new column to the DataFrame
    df[new_column_name] = mean_ages
    return df


'''
df = lobe_extraction(df,"Op_Type") 
df = clean_lobe_column(df) 
df = remove_rows_with_too_many_nans(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],1)
df = refill_nan_with_previous(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"])
included_df, excluded_df = filter_rows_by_conditions(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],[((1, 2), 4), ((3, 5), 4)])
#df = calculate_mean_age(df,"Binned_Onset_Age","mean_age")
print(included_df,excluded_df)
'''
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
