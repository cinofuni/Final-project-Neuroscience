import pandas as pd



def validate_columns(df, columns, valid_range):
    # Check if values are numeric and within the valid range
    is_numeric = df[columns].applymap(lambda x: isinstance(x, (int,float)))
    in_range = df[columns].applymap(lambda x: valid_range[0] <= x <= valid_range[1] if isinstance(x, (int,float)) else False)
    
    # Identify rows with invalid values
    invalid_rows = df[~(is_numeric & in_range).all(axis=1)]
    
    # Determine if all values are valid
    is_valid = invalid_rows.empty

    return is_valid, invalid_rows



def validate_lobe_column(df, column_name,valid_values):
    # Normalize both column values and valid_values to uppercase to handle case insensitivity
    valid_values = [x.upper() for x in valid_values]
    
    # Remove leading/trailing whitespaces from values (if any)
    df[column_name] = df[column_name].str.strip().str.upper()

    # Check if each value is valid (one of the valid values)
    is_valid = df[column_name].apply(lambda x: isinstance(x, str) and x in valid_values)
    
    # Get rows with invalid values
    invalid_rows = df[~is_valid]
    
    # Get the IDs of the rows with invalid values
    invalid_ids = invalid_rows["ID"].tolist() if not invalid_rows.empty else []

    # Return if all values are valid, list of invalid IDs, and the invalid rows themselves
    is_valid_all = invalid_rows.empty
    return is_valid_all, invalid_ids, invalid_rows



def get_unique_cell_values_with_nan(df, column_name):

    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Use pandas' unique() to get distinct values
    unique_values = df[column_name].unique()

    # Convert to a set and include NaN explicitly
    return set(unique_values)

#print(get_unique_cell_values_with_nan(df,"lobe"))

def get_unique_general(df,column_list):
    results = {}
    for column in column_list:
        unique_values = get_unique_cell_values_with_nan(df, column)
        results[column] = unique_values
        print(f"Unique values in column '{column}':")
        print(unique_values)
        print()  # Line break for better readability
    return results
    






