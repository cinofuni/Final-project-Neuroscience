import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import binomtest
import numpy as np
from data_cleaning import remove_rows_with_too_many_nans
from data_cleaning import refill_nan_with_previous
from data_cleaning import filter_rows_by_conditions
from data_cleaning import clean_lobe_column
df = pd.read_csv("C:/Users/Shimon Funaro/Downloads/Metadata_Release_Anon (1).csv")
df = remove_rows_with_too_many_nans(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],1)
df = refill_nan_with_previous(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"])
df["lobe"] = df["Op_Type"].str.extract(r"(T|F|O|P|)", expand = False)
df["operation"] = df["Op_Type"].str.extract(r"(Lx|Lesx|Hx)", expand = False)
df = filter_rows_by_conditions(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],[((1, 2), 4), ((3, 5), 4)])
df = clean_lobe_column(df)


def plotting(df,column,title,xlabel,ylabel):
    y_data = df[column].value_counts()
    y_data.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return plt.show()

print(plotting(df,["Op_Type"],["Op Type"],["unique values"],["Amount of patients"]))

'''
y_data = df["operation"].value_counts()
y_data.plot(kind="bar")
plt.title("Operation Type")
plt.xlabel("Operation")
plt.ylabel("Amount of patients")
plt.show()

y_data = df["Op_Type"].value_counts()
y_data.plot(kind="bar")
plt.title("Op Type")
plt.xlabel("unique values")
plt.ylabel("Amount of patients")
plt.show()

y_data = df["lobe"].value_counts()
print(y_data)
y_data.plot(kind="bar")
plt.title("Lobe Type")
plt.xlabel("Lobe")
plt.ylabel("Amount of patients")
plt.show()
print(y_data)
'''

