import pandas as pd
from data_cleaning import remove_rows_with_too_many_nans
from data_cleaning import refill_nan_with_previous
from data_cleaning import filter_rows_by_conditions
from data_cleaning import delete_row_by_id

df = pd.read_csv("C:/Users/Shimon Funaro/Downloads/Metadata_Release_Anon (1).csv")
df = pd.read_csv("C:/Users/Shimon Funaro/Downloads/Metadata_Release_Anon (1).csv")
df = remove_rows_with_too_many_nans(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],1)
df = refill_nan_with_previous(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"])
df["lobe"] = df["Op_Type"].str.extract(r"(T|F|O|P|)", expand = False)
df["operation"] = df["Op_Type"].str.extract(r"(Lx|Lesx|Hx)", expand = False)

def count_one_or_two_in_lobes(df, number_columns, letter_column):
    # Define a condition to count how many of the number columns have 1 or 2
    condition = df[number_columns].apply(lambda row: (row <= 2).sum(), axis=1) >= 4

    # Filter rows that satisfy the condition
    filtered_df = df[condition]

    # Count the occurrences of each letter
    letter_counts = filtered_df[letter_column].value_counts()

    # Total occurrences of each letter in the entire dataset
    total_counts = df[letter_column].value_counts()

    # Calculate percentages
    percentages = (letter_counts / total_counts * 100).fillna(0)

        # Combine counts and percentages into a DataFrame
    result = pd.DataFrame({
        'Count': letter_counts,
        'Percentage': percentages
    }).sort_index()

    return result

def count_three_to_five_in_lobes(df, number_columns, letter_column):
    # Define a condition to count how many of the number columns have values between 3 and 5
    condition = df[number_columns].apply(lambda row: ((row >= 3) & (row <= 5)).sum(), axis=1) >= 4

    # Filter rows that satisfy the condition
    filtered_df = df[condition]

    # Count the occurrences of each letter
    letter_counts = filtered_df[letter_column].value_counts()

    # Total occurrences of each letter in the entire dataset
    total_counts = df[letter_column].value_counts()

    # Calculate percentages
    percentages = (letter_counts / total_counts * 100).fillna(0)

        # Combine counts and percentages into a DataFrame
    result = pd.DataFrame({
        'Count': letter_counts,
        'Percentage': percentages
    }).sort_index()

    return result

df = filter_rows_by_conditions(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],[((1, 2), 4), ((3, 5), 4)])
df = delete_row_by_id(df,"ID", 326)
df = delete_row_by_id(df,"ID", 357)
lobe_count = count_one_or_two_in_lobes(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],["lobe"])
lobe_count2 = count_three_to_five_in_lobes(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],["lobe"])
print(lobe_count2,lobe_coun