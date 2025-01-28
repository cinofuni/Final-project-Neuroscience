'''Outsiders Imports'''
import pandas as pd


'''data saving and import'''
df = pd.read_csv("C:/Users/Shimon Funaro/Downloads/Metadata_Release_Anon (1).csv")


'''data_claning imports'''
from src.data_cleaning import lobe_extraction
from src.data_cleaning import clean_lobe_column
from src.data_cleaning import remove_rows_with_too_many_nans
from src.data_cleaning import refill_nan_with_previous
from src.data_cleaning import filter_rows_by_conditions
from src.data_cleaning import calculate_mean_age


'''operating the cleaning '''
df = lobe_extraction(df,"Op_Type") 
df = clean_lobe_column(df) 
df = remove_rows_with_too_many_nans(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],1)
df = refill_nan_with_previous(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"])
df = filter_rows_by_conditions(df,["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"],[((1, 2), 4), ((3, 5), 4)])
df = calculate_mean_age(df,"Binned_Onset_Age","mean_age")
print(df)


'''operating the testing for the cleaning'''
from tests.test_data_cleaning import get_unique_general


list_of_columns = ("Pathology","lobe","mean_age","ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5")
get_unique_general(df,list_of_columns)


'''operating the visualization '''
from src.data_visualisation import plotting

plotting(df,["Pathology"],["Pathology"],["Pathology Type"],["Amount of patients"])
plotting(df,["lobe"],["Lobes"],["Lobe Type"],["Amount of patients"])
plotting(df,["mean_age"],["Mean Age"],["The mean age of patient group"],["Amount of patients"])




'''Operating The Analysis'''

from src.data_analysis import general_analyze

general_analyze(df,["mean_age", "Pathology", "lobe"]) # Calling the function that will operate the analysis for each column



