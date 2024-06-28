#this file is responsible for the statistics and managment of the statsitics in the event. 


"""
TODO:
1: load in the data appropriately .... should filter match, regex strip, as well as posible 
2: possible
"""

import os
import pandas as pd


def print_directory_structure(root_dir, indent=''):
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            if item == 'streamlitVENV':
                continue
            print(f"{indent}{item}/")
            print_directory_structure(item_path, indent + '    ')
        else:
            print(f"{indent}{item}")


# Change 'project_root' to your actual project directory path
# project_root = '/Users/aaronfanous/Documents/MisinformationFiles/MisinformationRepo/streamLitDatadisplay'
# print_directory_structure(project_root)
import pandas as pd
import numpy as np

class LikertScaleAnalysis:
    def __init__(self, file_path):
        """
        Initializes the LikertScaleAnalysis class by loading the Excel file and preparing the data.
        
        Parameters:
        file_path (str): Path to the Excel file.
        """
        self.file_path = file_path
        self.data = self._load_file()
        self._create_sample_id()
    
    def _load_file(self):
        """
        Loads the Excel file and returns the data from the first sheet.
        
        Returns:
        pd.DataFrame: DataFrame for the first sheet.
        """
        xls = pd.ExcelFile(self.file_path)
        data = pd.read_excel(xls, sheet_name='Sheet1')
        return data

    def _create_sample_id(self):
        """
        Creates a sample ID for each row in the DataFrame.
        """
        self.data['SampleID'] = self.data.apply(
            lambda row: f"{row['Subreddit']}_{row['Reddit Post ID']}_{row['Comment ID']}", axis=1)
    
    def create_pivot_tables(self, aggfunc='first'):
        """
        Creates pivot tables for each question, organizing data by SampleID and Username.
        
        Parameters:
        aggfunc (str or function): Aggregation function to use for pivoting data.
        
        Returns:
        dict: Dictionary of pivot tables for each question.
        """
        questions = ['Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5']
        pivoted_data = {}
        for question in questions:
            pivoted_data[question] = self.data.pivot_table(index='SampleID', columns='Username', values=question, aggfunc=aggfunc)
        return pivoted_data

    def calculate_krippendorff_alpha(self, pivoted_data):
        """
        Calculates Krippendorff's Alpha for interrater reliability for each question.
        
        Parameters:
        pivoted_data (dict): Dictionary of pivot tables for each question.
        
        Returns:
        dict: Dictionary of Krippendorff's Alpha values for each question.
        """
        alphas = {}
        for question, df in pivoted_data.items():
            # Drop rows with missing values
            df_cleaned = df.dropna(axis=0, how='any')
            if df_cleaned.empty:
                alphas[question] = np.nan
                continue
            # Convert the DataFrame to a matrix
            data_matrix = df_cleaned.values
            alphas[question] = self._krippendorff_alpha(data_matrix)
        return alphas
    
    def _krippendorff_alpha(self, data):
        """
        Computes Krippendorff's Alpha for a given data matrix.
        
        Parameters:
        data (np.array): 2D array where rows are samples and columns are raters.
        
        Returns:
        float: Krippendorff's Alpha value.
        """
        def nominal_metric(a, b):
            return np.sum(a != b)

        def observed_disagreement(data, metric):
            pairs = [(i, j) for i in range(data.shape[1]) for j in range(i + 1, data.shape[1])]
            disagreements = [metric(data[:, i], data[:, j]) for i, j in pairs]
            total_pairs = len(pairs) * data.shape[0]
            return np.sum(disagreements) / total_pairs

        def expected_disagreement(data, metric):
            n, k = data.shape
            categories = np.unique(data)
            observed_frequencies = {cat: np.sum(data == cat) for cat in categories}
            total_observations = n * k
            expected_disagreement = 0

            for i in categories:
                for j in categories:
                    if i != j:
                        expected_disagreement += (observed_frequencies[i] * observed_frequencies[j]) / (total_observations - 1)
            
            expected_disagreement /= total_observations
            return expected_disagreement

        D_o = observed_disagreement(data, nominal_metric)
        D_e = expected_disagreement(data, nominal_metric)
        return 1 - D_o / D_e if D_e != 0 else 1

# Example usage:
file_path = "/Users/aaronfanous/Documents/MisinformationFiles/MisinformationRepo/streamLitDatadisplay/data/raw/HumanRepsonsesRaw/PromptSysReviewPresentation.xlsx"
analysis = LikertScaleAnalysis(file_path)
pivot_tables = analysis.create_pivot_tables()
alphas = analysis.calculate_krippendorff_alpha(pivot_tables)
# print(pivot_tables)
# print(alphas)


import pandas as pd
import krippendorff

# Load the provided file
file_path = "/Users/aaronfanous/Documents/MisinformationFiles/MisinformationRepo/streamLitDatadisplay/data/raw/HumanRepsonsesRaw/PromptSysReviewPresentation.xlsx"
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Convert category strings to numerical values
rating_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}
data['SampleID'] = data.apply(
            lambda row: f"{row['Subreddit']}_{row['Reddit Post ID']}_{row['Comment ID']}", axis=1)
def group_values(rating):
    if rating in [4, 5]:
        return 3
    elif rating in [1, 2]:
        return 1
    elif rating in [3]:
        return 2
    else:
        return rating

# Apply the grouping to the entire matrix
grouped_data = np.vectorize(group_values)(data)
def percent_agreement(matrix):
    agreement_counts = []
    
    for col in range(matrix.shape[1]):
        ratings = matrix[:, col]  # Get all ratings for the current sample (column)
        mode = np.bincount(ratings).argmax()  # Calculate the mode (most common rating)
        agreement = (ratings == mode).sum() / len(ratings)  # Calculate the agreement percentage
        agreement_counts.append(agreement)
        
    return np.mean(agreement_counts), agreement_counts


for question in ['Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5']:
    
    data[question] = data[question].map(rating_map)

# Create pivot table for Q1
for question in [ 'Q1', 'Q2', 'Q3', 'Q4', 'Q5']:
    pivot_table_Q1 = data.pivot_table(index='SampleID', columns='Username', values=question, aggfunc='first')
    

    # Clean the pivot table by dropping rows with any missing values
    cleaned_pivot_table_Q1 = pivot_table_Q1.dropna(axis=0, how='any').transpose()
    
    # Convert the cleaned pivot table to a matrix
    data_matrix_Q1 = cleaned_pivot_table_Q1.values.astype(int)

  

# Apply the grouping to the entire matrix
    grouped_data = np.vectorize(group_values)(data_matrix_Q1)
    
    overall_agreement, sample_agreements = percent_agreement(grouped_data)

    print(f"Overall Percent Agreement: {overall_agreement:.2f}")
    value_counts = np.apply_along_axis(lambda x: np.bincount(x, minlength=4), axis=0, arr=grouped_data)
    value_counts=value_counts.transpose()
    # Calculate Krippendorff's Alpha using the krippendorff package
    
    alpha = krippendorff.alpha(value_counts=value_counts, level_of_measurement='ordinal')

# Print the results
    print(f"Krippendorff's Alpha for {question} using krippendorff package: {alpha}")

import pandas as pd
from CACpackages import CAC
# Example ordinal data
# data = pd.DataFrame({
#     'Rater1': [1, 2, 3, 4, 2, 1, 4, 1, 2, 5, 1, 3],
#     'Rater2': [1, 2, 3, 4, 2, 2, 4, 1, 2, 5, 1, 3],
#     'Rater3': [None, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, None],
#     'Rater4': [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, None]
# })

# Initialize CAC object with ordinal weights
# cac = CAC(data, weights="ordinal")

# # Calculate Gwet's AC2
# gwet_ac2_result = cac.gwet()
# print("Gwet's AC2 Result:", gwet_ac2_result)
for question in [ 'Q1', 'Q2', 'Q3', 'Q4', 'Q5']:
    pivot_table_Q1 = data.pivot_table(index='SampleID', columns='Username', values=question, aggfunc='first')
    

    # Clean the pivot table by dropping rows with any missing values
    cleaned_pivot_table_Q1 = pivot_table_Q1.dropna(axis=0, how='any').transpose()
    
    # Convert the cleaned pivot table to a matrix
    data_matrix_Q1 = cleaned_pivot_table_Q1.values.astype(int)
    cac = CAC(cleaned_pivot_table_Q1, weights="ordinal")
# Calculate Gwet's AC2

    gwet_ac2_result = cac.gwet()
    print(f"Gwet's {question} AC2 Result:{gwet_ac2_result}")