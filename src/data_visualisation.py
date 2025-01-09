import matplotlib.pyplot as plt
from data_cleaning import lobe_extraction 
from data_cleaning import remove_rows_with_too_many_nans
from data_cleaning import fill_nans_with_row_mean
import pandas as pd 

df = pd.read_csv("C:/Users/Shimon Funaro/Downloads/Metadata_Release_Anon (1).csv")
df = remove_rows_with_too_many_nans(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],2)
df = fill_nans_with_row_mean(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"])

df["lobe"] = df["Op_Type"].str.extract(r"(T|F|O|P|)", expand = False)

y_data = df["lobe"].value_counts()
y_data.plot(kind="bar")
plt.title("Lobe Type")
plt.xlabel("Lobe")
plt.ylabel("Amount of patients")
plt.show()

df["operation"] = df["Op_Type"].str.extract(r"(Lx|Lesx|Hx)", expand = False)

y_data = df["operation"].value_counts()
y_data.plot(kind="bar")
plt.title("Operation Type")
plt.xlabel("Operation")
plt.ylabel("Amount of patients")
plt.show()

