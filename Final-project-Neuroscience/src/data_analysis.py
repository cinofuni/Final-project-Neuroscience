import pandas as pd
#from scipy.stats import proportions_ztest
from scipy.stats import binomtest
import numpy as np
import matplotlib as plt


df = pd.read_csv("C:/Users/Shimon Funaro/Downloads/Metadata_Release_Anon (1).csv")


'''Analisys for the cleaned data'''


def count_by_range(df, number_columns, letter_column, lower_range, upper_range):

    # Define the condition to count how many columns are within the range
    condition = df[number_columns].apply(lambda row: ((row >= lower_range) & (row <= upper_range)).sum(), axis=1) >= 4

    # Filter rows that satisfy the condition
    filtered_df = df[condition]

    # Count the occurrences of each unique value in `letter_column`
    letter_counts = filtered_df[letter_column].value_counts()

    # Total occurrences of each unique value in the entire dataset
    total_counts = df[letter_column].value_counts()

    # Calculate percentages
    percentages = (letter_counts / total_counts * 100).fillna(0)

    # Combine counts and percentages into a DataFrame
    result = pd.DataFrame({
        'Count': letter_counts.astype(int),
        'Percentage': percentages
    }).sort_index()

    return result


'''
def analyze_column_significant_only(good_data, bad_data,column):

    our_column = good_data.index.intersection(bad_data.index)  # Ensure matching lobes
    results = []

    for type in our_column:
        good_count = good_data.loc[type, 'Count']
        bad_count = bad_data.loc[type, 'Count']
        total_count = good_count + bad_count

        # Perform binomial test
        stat = binomtest(k=int(good_count), n=int(total_count), p=0.5, alternative='two-sided')
        p_value = stat.pvalue

        # Check significance
        if p_value < 0.05:
            results.append({
                "column": type,
                "Good Count": good_count,
                "Bad Count": bad_count,
                "P-value": p_value,
                "Significant": True,
            })

            # Print only significant results
            print(f"Found significant difference between good and bad counts for {column} {type}.")
            print(f"Good Count: {good_count}, Bad Count: {bad_count}")
            print(f"P-value: {p_value:.10f}")
            print("-" * 50)

    return results

'''




def analyze_column_significant_only(good_data, bad_data, column, return_type=1):
    our_column = good_data.index.intersection(bad_data.index)  # Ensure matching lobes
    results = []

    for type in our_column:
        good_count = good_data.loc[type, 'Count']
        bad_count = bad_data.loc[type, 'Count']
        total_count = good_count + bad_count

        # Perform binomial test
        stat = binomtest(k=int(good_count), n=int(total_count), p=0.5, alternative='two-sided')
        p_value = stat.pvalue

        # Determine significance
        significant = p_value < 0.05

        result = {
            "column": type,
            "Good Count": good_count,
            "Bad Count": bad_count,
            "P-value": p_value,
            "Significant": significant,
        }
        results.append(result)

        # Print only significant results when return_type is 1
        if significant and return_type == 1:
            print(f"Found significant difference between good and bad counts for {column} {type}.")
            print(f"Good Count: {good_count}, Bad Count: {bad_count}")
            print(f"P-value: {p_value:.10f}")
            print("-" * 50)

    # Filter results if return_type is 1
    if return_type == 1:
        results = [res for res in results if res["Significant"]]

    return results


# A function that calls and runs all the analyze functions for each column
def general_analyze(df,columns):
    list = ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"]
    for column in columns:
        good_count = count_by_range(df,list,column,1,2)
        bad_count = count_by_range(df,list,column,3,5)
        analyze_column_significant_only(good_count,bad_count,column)




'''Analysis for the excluded data'''



def check_commonality_with_comparison(df, excluded_df, threshold=0.8):

    common_values = {}
    total_rows_before = len(df)
    total_rows_after = len(excluded_df)
    threshold_count_before = total_rows_before * threshold  # Threshold based on original DataFrame

    print(f"Original number of rows: {total_rows_before}")
    print(f"Filtered number of rows: {total_rows_after}")
    
    for column in df.columns:
        if df[column].dtype == 'object':  # Check only categorical columns (e.g., strings)
            # Count unique values before filtering (in the original DataFrame)
            value_counts_before = df[column].value_counts()
            
            # Count unique values after filtering (in the excluded DataFrame)
            value_counts_after = excluded_df[column].value_counts()

            for value, count_before in value_counts_before.items():
                count_after = value_counts_after.get(value, 0)
                
                # Check if the count of this value after filtering meets the threshold percentage of the original count
                if count_after >= threshold_count_before:
                    common_values[column] = value
                    print(f"Common value found in '{column}': {value}")
                    print(f"Before filtering: {count_before} occurrences")
                    print(f"After filtering: {count_after} occurrences")
                    print("-" * 50)
    
    # If there are common values found, print them
    if common_values:
        print("Common values found across the DataFrame after filtering:")
        for column, value in common_values.items():
            print(f"{column}: {value}")
    else:
        print("No common values found based on the threshold.")
    
    return common_values




def plot_general_analyze_results_all(df, columns):

    list_columns = ["ILAE_Year1", "ILAE_Year2", "ILAE_Year3", "ILAE_Year4", "ILAE_Year5"]

    for column in columns:
        print(f"Analyzing and plotting column: {column}")
        
        # Calculate "good" and "bad" counts
        good_count = count_by_range(df, list_columns, column, 1, 2)
        bad_count = count_by_range(df, list_columns, column, 3, 5)
        
        # Perform analysis
        results  = analyze_column_significant_only(good_count, bad_count, column,2)
        
        # If results exist, plot them
        if results:
            print(f"Generating plot for column: {column}")
            # Prepare data for visualization
            categories = [str(res["column"]) for res in results]
            p_values = [res["P-value"] for res in results]
            significance = ["red" if res["P-value"] < 0.05 else "blue" for res in results]

            # Plot all p-values
            plt.figure(figsize=(12, 6))
            #plt.plot(categories, p_values, marker="o", linestyle="-", color="black", alpha=0.7)
            plt.scatter(categories, p_values, color=significance, s=100, label="P-value")

            # Highlight significance threshold
            plt.axhline(y=0.05, color="orange", linestyle="--", label="Significance Threshold (p=0.05)")

            # Chart settings
            plt.title(f"P-Values for {column}", fontsize=16)
            plt.xlabel("Categories", fontsize=12)
            plt.ylabel("P-value", fontsize=12)
            plt.xticks(rotation=45, ha="right")
            plt.ylim(0, 1)  # P-values range from 0 to 1
            plt.legend()
            plt.grid(axis="y", linestyle="--", alpha=0.7)

            plt.tight_layout()
            plt.show()
        else:
            print(f"No results to plot for column: {column}")

#columns_to_analyze = ["lobe", "Pathology","mean_age"]
#plot_general_analyze_results_all(df, columns_to_analyze)






