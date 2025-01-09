import pandas as pd
from data_cleaning import remove_rows_with_too_many_nans
from data_cleaning import fill_nans_with_row_mean

df = pd.read_csv("C:/Users/Shimon Funaro/Downloads/Metadata_Release_Anon (1).csv")
df = pd.read_csv("C:/Users/Shimon Funaro/Downloads/Metadata_Release_Anon (1).csv")
df = remove_rows_with_too_many_nans(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],2)
df = fill_nans_with_row_mean(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"])
df["lobe"] = df["Op_Type"].str.extract(r"(T|F|O|P|)", expand = False)
df["operation"] = df["Op_Type"].str.extract(r"(Lx|Lesx|Hx)", expand = False)



def calculate_group_averages(df, group_column, columns_to_average):
    group_averages = df.groupby(group_column)[columns_to_average].mean()
    combined_average = group_averages.mean(axis=1)
    return combined_average

dg = calculate_group_averages(df,"lobe", ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"])
print(dg)
gg = calculate_group_averages(df,"operation", ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"])
print(gg)