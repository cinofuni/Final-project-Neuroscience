import matplotlib.pyplot as plt
import pandas as pd
from src.data_analysis import count_by_range
from tests.ensuring_data import get_unique_cell_values_with_nan
from src.data_analysis import analyze_column_significant_only

''' Plotting the good and bad for each collumn '''

def plotting_with_good_and_bad(
    df,  
    letter_column, 
    title, 
    xlabel, 
    ylabel = "Count", 
    good_range=(1, 2), 
    bad_range=(3, 5)
):

    # Get "Good" and "Bad" data counts using count_by_range
    good_data = count_by_range(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"], letter_column, *good_range)['Count']
    bad_data = count_by_range(df, ["ILAE_Year1","ILAE_Year2","ILAE_Year3","ILAE_Year4","ILAE_Year5"], letter_column, *bad_range)['Count']

    # Combine data into a single DataFrame for plotting
    combined_data = pd.DataFrame({
        "Good": good_data,
        "Bad": bad_data
    }).fillna(0)  # Fill NaN with 0 for plotting purposes

    # Plot side-by-side bars
    combined_data.plot(kind="bar", figsize=(10, 6), color=["skyblue", "salmon"])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)

    # Annotate bars with counts
    for idx, (good, bad) in enumerate(zip(combined_data['Good'], combined_data['Bad'])):
        plt.text(idx - 0.2, good + 1, int(good), ha='center', va='bottom', fontsize=10, color='blue')
        plt.text(idx + 0.2, bad + 1, int(bad), ha='center', va='bottom', fontsize=10, color='red')

    plt.legend(["Good (1-2)", "Bad (3-5)"])
    plt.tight_layout()
    plt.show()



def plot_multiple_columns_with_good_and_bad(
    df,  
    letter_columns, 
    good_range=(1, 2), 
    bad_range=(3, 5)
):

    for letter_column in letter_columns:
        # Generate a title specific to the column
        title = f"{letter_column}: Distribution - Good (1-2) vs Bad (3-5)"
        
        # Call the plotting function
        plotting_with_good_and_bad(
            df=df,
            letter_column=letter_column,
            title=title,
            xlabel=letter_column,
            ylabel="Count",
            good_range=good_range,
            bad_range=bad_range
        )




'''we will see hahahaha'''

def plot_lobe_distribution_per_pathology(df, pathology_column, lobe_column):

    # Get unique pathologies
    unique_pathologies = get_unique_cell_values_with_nan(df, pathology_column)

    for pathology in unique_pathologies:
        if pd.isna(pathology):  # Skip NaN values
            continue

        # Filter data for the current pathology
        filtered_data = df[df[pathology_column] == pathology]

        # Count occurrences of each lobe
        lobe_counts = filtered_data[lobe_column].value_counts()

        # Plot pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(
            lobe_counts,
            labels=lobe_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],  # Assign custom colors
        )
        plt.title(f"Lobe Distribution for Pathology: {pathology}")
        plt.show()




'''we will also see hahahaha'''


def visualize_binomial_p_values(results, title="P-Values from Binomial Test"):
    if not results:
        print("No significant results to visualize.")
        return

    # Extract data for visualization
    categories = [str(res["column"]) for res in results]  # Convert to strings
    p_values = [res["P-value"] for res in results]
    significance = ["red" if res["Significant"] else "blue" for res in results]

    # Debugging output
    print("Categories:", categories)
    print("P-values:", p_values)

    # Plot p-values
    plt.figure(figsize=(12, 6))
    #plt.plot(categories, p_values, marker="o", linestyle="-", color="black", alpha=0.7)
    plt.scatter(categories, p_values, color=significance, s=100, label="P-value")

    # Highlight significance threshold
    plt.axhline(y=0.05, color="orange", linestyle="--", label="Significance Threshold (p=0.05)")

    # Chart settings
    plt.title(title, fontsize=16)
    plt.xlabel("Categories", fontsize=12)
    plt.ylabel("P-value", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.ylim(0, 1)  # P-values range from 0 to 1
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()





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





