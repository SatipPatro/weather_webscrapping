import os
import pandas as pd
from bs4 import BeautifulSoup

# Define the base directory containing the HTML files
base_directory = 'D:/Events/Droughts'

# Define a function to parse the HTML and extract table data based on table id
def parse_html_to_df(file_path, table_id):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        table = soup.find('table', {'id': table_id}) or soup.find('div', {'id': table_id}).find('table')
        
        if not table:  # Handle case where the table isn't found
            print(f"Table with id '{table_id}' not found in {file_path}.")
            return None
        
        # Extract headers
        headers = [th.text.strip() for th in table.find('tr').find_all('th')]
        
        # Extract rows
        rows = []
        for tr in table.find_all('tr')[1:]:  # Skip header row
            cells = [td.get_text(separator=' ').strip() for td in tr.find_all('td')]
            rows.append(cells)
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)
        return df

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# List of table IDs to extract
table_ids = ['ctl00_CPH_GridViewEpisodes', 'countries', 'aru']

# Iterate over each table ID
for table_id in table_ids:
    all_data_frames = []
    
    # Directory for the specific table
    specific_directory = os.path.join(base_directory, table_id)
    create_directory(specific_directory)
    
    # Iterate over files in the base directory
    for file_name in os.listdir(base_directory):
        if file_name.endswith('.html'):
            file_path = os.path.join(base_directory, file_name)
            df = parse_html_to_df(file_path, table_id)
            if df is not None:
                all_data_frames.append(df)
    
    # Combine all DataFrames into one
    if all_data_frames:  # Proceed only if DataFrames were found
        combined_df = pd.concat(all_data_frames, ignore_index=True)
        
        # Save the combined DataFrame to a CSV file in the specific directory
        csv_file_path = os.path.join(specific_directory, f'{table_id}_data.csv')
        combined_df.to_csv(csv_file_path, index=False, encoding='utf-8')
        print(f'Data extraction and CSV creation completed successfully for table id: {table_id}')
    else:
        print(f'No data found for table id: {table_id}')

print('All data extraction and CSV creation tasks completed.')
