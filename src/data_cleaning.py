import pandas as pd

#instaling the excel file
df = pd.read_csv("C:/Users/Shimon Funaro/Downloads/Metadata_Release_Anon (1).csv")

# a function to identify rows with too many NaN values in specific columns and delete them
def remove_rows_with_too_many_nans(df, columns, max_allowed_nans):

   # Count the number of NaNs in the specified columns for each row
    nan_counts = df[columns].isna().sum(axis=1)
    
    # Filter rows where the NaN count exceeds the allowed maximum of two
    cleaned_df = df[nan_counts <= max_allowed_nans].copy()
    
    return cleaned_df

# a function that will refill the Nan's that are in the colunms with the mean of the rest of the factors that patient
def fill_nans_with_row_mean(df, columns):
    def row_median_fill(row):
        # Compute the median of the specified columns for the current row
        mean_value = row[columns].mean(skipna=True)
        # Fill NaN values in the row with the computed median
        row[columns] = row[columns].fillna(mean_value)
        return row

    # Apply the function row by row
    df = df.apply(row_median_fill, axis=1)
    return df

#creating a new colunm with the lobe the patient had an operation on
def lobe_extraction():
    df["lobe"] = df["Op_Type"].str.extract(r"(T|F|O|P|)", expand = False)
    return (df["lobe"])

#creating a new colunm with the operation type the patient had 
def Op_type_extraction():
    df["operation"] = df["Op_Type"].str.extract(r"(Lx|Lesx|Hx)", expand = False)
    return (df["operation"])

cleande = remove_rows_with_too_many_nans(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],2)
df = fill_nans_with_row_mean(cleande,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"])
print(lobe_extraction())




