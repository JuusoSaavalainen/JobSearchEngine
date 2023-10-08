import os
import pandas as pd
import csv

# Reads all csv files from data folder and merges them into one csv file containing only unique rows

folder_path = 'data/'
all_dataframes = []

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        try:
            df = pd.read_csv(file_path)
            if not df.empty:
                all_dataframes.append(df)
                print(f"File {filename} has been loaded successfully")
        except pd.errors.EmptyDataError:
            print(f"Skipping empty file: {file_path}")

merged_df = pd.concat(all_dataframes, ignore_index=True)
merged_df = merged_df.drop_duplicates(subset='description')
merged_df.to_csv(f'uniquejobs.csv', index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
